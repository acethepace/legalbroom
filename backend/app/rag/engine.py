import os
import re
import json
from typing import List, Dict, Any, AsyncGenerator, Optional
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from app.services.courtlistener import CourtListenerService
from app.rag.factory import LLMFactory

@tool
def search_courtlistener(query: str):
    """
    Search CourtListener for legal precedent, case law, and citations.
    Use this tool when the user's question requires information about existing legal cases, 
    precedents, or general legal principles not found in the provided document.
    """
    return "Searching..."

class RAGEngine:
    def __init__(self, courtlistener_service: Optional[CourtListenerService] = None):
        self.courtlistener_service = courtlistener_service
        self.llm = LLMFactory.get_model()

    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "EMPTY - NO DOCUMENT UPLOADED"
        formatted_context = ""
        for i, chunk in enumerate(chunks):
            formatted_context += f"--- Source {i+1} ---\n"
            formatted_context += f"Section: {chunk.get('section_title', 'N/A')}\n"
            formatted_context += f"Text: {chunk.get('text', '')}\n\n"
        return formatted_context

    def _prepare_initial_citations(self, context_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        formatted_citations = []
        for i, chunk in enumerate(context_chunks):
            bbox = chunk.get("bboxes", [None])[0] if chunk.get("bboxes") else None
            coords = None
            if bbox and len(bbox) >= 4:
                coords = {
                    "x": bbox[0],
                    "y": bbox[1],
                    "w": bbox[2] - bbox[0],
                    "h": bbox[3] - bbox[1]
                }
                
            formatted_citations.append({
                "id": str(i + 1),
                "snippet": chunk.get("text", ""),
                "pageNumber": chunk.get("page_numbers", [1])[0] if chunk.get("page_numbers") else 1,
                "title": f"Source {i+1}",
                "court": "Uploaded Document",
                "date_filed": "N/A",
                "url": "",
                "coordinates": coords
            })
        return formatted_citations

    async def stream_answer(self, question: str, context_chunks: List[Dict[str, Any]]) -> AsyncGenerator[Dict[str, Any], None]:
        yield {"type": "status", "text": "Analyzing query..."}
        
        context_str = self._format_context(context_chunks)
        
        system_prompt = f"""
You are a professional legal assistant. You have access to the `search_courtlistener` tool for finding legal precedents and case law.

MANDATORY: You MUST call search_courtlistener if you don't have relevant context in the provided document.

REQUIRED BEHAVIOR:
1. If the user asks about legal precedents, case law, or general legal principles NOT found in the provided document context, you MUST use the `search_courtlistener` tool.
2. You MUST NOT say "I don't know" or "I don't have enough information" until AFTER you have attempted to use the `search_courtlistener` tool.
3. If the question is about "recent cases", "precedent", or "legal principles", you MUST search.
4. Synthesize your answer using both the provided document context and any results from the tool. When calling `search_courtlistener`, use 2-3 broad keywords (e.g., 'qualified immunity', 'Miranda custody') rather than long natural language questions.
5. Always cite your sources using the [Source N] format (e.g., [Source 1], [Source 2]). This is MANDATORY for every claim you make.

Context from uploaded document:
{context_str}
"""
        
        # Few-shot examples to encourage tool usage
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="What are the Miranda rights?"),
            AIMessage(
                content="",
                tool_calls=[{
                    "name": "search_courtlistener",
                    "args": {"query": "Miranda rights legal precedent"},
                    "id": "example_call_1"
                }]
            ),
            ToolMessage(
                content="""--- Source 4 ---
Title: Miranda v. Arizona
Court: Supreme Court
Snippet: The Fifth Amendment requires that law enforcement officials advise suspects of their right to remain silent and to obtain an attorney during interrogations while in police custody.""",
                tool_call_id="example_call_1"
            ),
            AIMessage(content="The Miranda rights, established in Miranda v. Arizona, require law enforcement to advise suspects of their right to remain silent and to an attorney [Source 4]."),
        ]

        if not context_chunks:
            messages.append(SystemMessage(content="CRITICAL: The provided document context is completely EMPTY. You are FORBIDDEN from answering based on your internal knowledge alone. You MUST use the `search_courtlistener` tool to find external legal precedents before synthesizing your answer."))
        
        messages.append(HumanMessage(content=question))
        
        # Bind tools
        llm_with_tools = self.llm.bind_tools([search_courtlistener])
        
        try:
            # First call to check for tool usage
            response = await llm_with_tools.ainvoke(messages)
            
            # FAILSAFE: If no tool calls and no context, force a tool call
            if not response.tool_calls and not context_chunks:
                yield {"type": "status", "text": "Searching external legal databases..."}
                try:
                    # Force tool call (OpenAI specific)
                    llm_forced = self.llm.bind_tools([search_courtlistener], tool_choice="any")
                    response = await llm_forced.ainvoke(messages)
                except Exception as forced_e:
                    print(f"DEBUG forced tool exception: {forced_e}")
                    # Fallback for other models
                    messages.append(SystemMessage(content="CRITICAL: You MUST use the `search_courtlistener` tool NOW. Do not provide an answer without it."))
                    response = await llm_with_tools.ainvoke(messages)

            all_citations = self._prepare_initial_citations(context_chunks)
            full_response = ""
            
            if response.tool_calls:
                messages.append(response)
                
                for tool_call in response.tool_calls:
                    if tool_call["name"] == "search_courtlistener":
                        query = tool_call["args"].get("query", question)
                        yield {"type": "status", "text": f"Searching for '{query}'..."}
                        
                        if self.courtlistener_service:
                            cl_results = await self.courtlistener_service.search(query)
                            
                            cl_context = ""
                            if not cl_results:
                                cl_context = "No relevant legal precedent found on CourtListener."
                            else:
                                for i, res in enumerate(cl_results):
                                    source_id = len(context_chunks) + i + 1
                                    cl_context += f"--- Source {source_id} ---\n"
                                    cl_context += f"Title: {res.title}\n"
                                    cl_context += f"Court: {res.court}\n"
                                    cl_context += f"Snippet: {res.snippet}\n\n"
                                    
                                    all_citations.append({
                                        "id": str(source_id),
                                        "snippet": res.snippet,
                                        "pageNumber": 1,
                                        "title": res.title,
                                        "court": res.court,
                                        "date_filed": res.date_filed,
                                        "url": res.url
                                    })
                            
                            messages.append(ToolMessage(content=cl_context, tool_call_id=tool_call["id"]))
                        else:
                            messages.append(ToolMessage(content="CourtListener service not available.", tool_call_id=tool_call["id"]))
                
                yield {"type": "status", "text": "Synthesizing answer..."}
                async for chunk in self.llm.astream(messages):
                    if chunk.content:
                        full_response += chunk.content
                        yield {"type": "content", "text": chunk.content}
            else:
                # No tool call, just stream the initial response content if it exists
                if response.content:
                    full_response += response.content
                    yield {"type": "content", "text": response.content}
                else:
                    # Fallback if content is empty
                    async for chunk in self.llm.astream(messages):
                        if chunk.content:
                            full_response += chunk.content
                            yield {"type": "content", "text": chunk.content}

            # Filter citations based on what was actually cited
            cited_ids = set(re.findall(r"\[Source (\d+)\]", full_response))
            filtered_citations = [c for c in all_citations if c["id"] in cited_ids]

            # Yield all citations
            yield {
                "type": "citations",
                "payload": filtered_citations
            }

        except Exception as e:
            yield {
                "type": "error",
                "text": f"Error in RAG Engine: {str(e)}"
            }

    async def stream_case_analysis(self, case_details: str) -> AsyncGenerator[Dict[str, Any], None]:
        try:
            yield {"type": "status", "text": "Analyzing case details..."}
            
            if not self.courtlistener_service:
                yield {"type": "error", "text": "CourtListener service not available."}
                return

            system_message = SystemMessage(content="You are a professional legal expert specializing in case analysis and precedent research.")

            # 1. Extract initial keywords for search
            yield {"type": "status", "text": "Extracting search queries..."}
            query_prompt = f"""
Based on the following case details, extract 1-2 specific legal keywords (e.g., 'qualified immunity', 'breach of contract') to find relevant precedents.
Output ONLY the queries separated by commas.

Case Details:
{case_details}
"""
            query_response = await self.llm.ainvoke([system_message, HumanMessage(content=query_prompt)])
            queries = [q.strip() for q in query_response.content.split(',')]
            current_query = queries[0] if queries else case_details[:50]
            
            accumulated_results = []
            all_citations = []
            iteration = 0
            max_iterations = 3
            needs_more_search = True
            total_results_seen = 0
            
            while needs_more_search and iteration < max_iterations:
                iteration += 1
                if iteration > 1:
                    yield {"type": "status", "text": "Refining search..."}
                
                yield {"type": "status", "text": f"Searching for '{current_query}'..."}
                cl_results = await self.courtlistener_service.search(current_query)
                
                if not cl_results:
                    if iteration == 1:
                        yield {"type": "content", "text": "No relevant legal precedent found on CourtListener for these case details."}
                        return
                    else:
                        break
                
                # 3. Grade Relevance and decide if more search is needed
                yield {"type": "status", "text": "Grading case relevance..."}
                
                cases_context = ""
                batch_start_id = total_results_seen + 1
                for i, res in enumerate(cl_results):
                    source_id = batch_start_id + i
                    cases_context += f"--- Source {source_id} ---\n"
                    cases_context += f"Title: {res.title}\n"
                    cases_context += f"Court: {res.court}\n"
                    cases_context += f"Snippet: {res.snippet}\n\n"

                grading_prompt = f"""
You are a legal expert evaluating the relevance of precedents to a specific case.
Review the following case details and the retrieved precedents.
Identify which precedents are relevant to the case details.

Output ONLY a JSON object with the following keys:
- "relevant_ids": List of Source IDs (integers ONLY) that are relevant.
- "needs_more_search": Boolean, true if the current results are insufficient and a different search query might find better results.
- "next_search_query": String, a refined search query if needs_more_search is true, otherwise empty string.

Case Details:
{case_details}

Retrieved Precedents:
{cases_context}
"""
                grading_response = await self.llm.ainvoke([system_message, HumanMessage(content=grading_prompt)])
                
                try:
                    # Extract JSON object from response
                    json_match = re.search(r'\{.*\}', grading_response.content, re.DOTALL)
                    if json_match:
                        grading_data = json.loads(json_match.group(0))
                        
                        # Robust ID parsing
                        relevant_ids = []
                        for raw_id in grading_data.get("relevant_ids", []):
                            match = re.search(r'\d+', str(raw_id))
                            if match:
                                relevant_ids.append(int(match.group()))
                        
                        needs_more_search = bool(grading_data.get("needs_more_search", False))
                        current_query = str(grading_data.get("next_search_query", ""))
                    else:
                        relevant_ids = []
                        needs_more_search = False
                except Exception as e:
                    print(f"Error parsing grading response: {e}")
                    # Fallback: assume current batch is relevant and stop searching
                    relevant_ids = list(range(batch_start_id, batch_start_id + len(cl_results)))
                    needs_more_search = False
                
                # Filter and accumulate results
                for i, res in enumerate(cl_results):
                    source_id = batch_start_id + i
                    if source_id in relevant_ids:
                        accumulated_results.append(res)
                        all_citations.append({
                            "id": str(source_id),
                            "snippet": res.snippet,
                            "pageNumber": 1,
                            "title": res.title,
                            "court": res.court,
                            "date_filed": res.date_filed,
                            "url": res.url
                        })
                
                total_results_seen += len(cl_results)
                
                if not needs_more_search:
                    break

            if not accumulated_results:
                yield {"type": "content", "text": "Found precedents, but none were deemed relevant to your specific case details."}
                return

            # 4. Final Synthesis
            yield {"type": "status", "text": "Synthesizing answer..."}
            
            filtered_context = ""
            for citation in all_citations:
                filtered_context += f"--- Source {citation['id']} ---\n"
                filtered_context += f"Title: {citation['title']}\n"
                filtered_context += f"Court: {citation['court']}\n"
                filtered_context += f"Snippet: {citation['snippet']}\n\n"

            synthesis_prompt = f"""
You are a professional legal assistant.
Analyze the following case details and provide a comprehensive legal analysis based ONLY on the provided relevant precedents.
Always cite your sources using the [Source N] format (e.g., [Source 1], [Source 2]). This is MANDATORY for every claim you make.

Case Details:
{case_details}

Relevant Precedents:
{filtered_context}
"""
            
            full_response = ""
            async for chunk in self.llm.astream([system_message, HumanMessage(content=synthesis_prompt)]):
                if chunk.content:
                    full_response += chunk.content
                    yield {"type": "content", "text": chunk.content}
                    
            # Filter citations based on what was actually cited
            cited_ids = set(re.findall(r"\[Source (\d+)\]", full_response))
            filtered_citations = [c for c in all_citations if c["id"] in cited_ids]

            # Yield all citations
            yield {
                "type": "citations",
                "payload": filtered_citations
            }
        except Exception as e:
            yield {
                "type": "error",
                "text": f"Error in RAG Engine: {str(e)}"
            }


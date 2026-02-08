from google.genai import types
from duckduckgo_search import DDGS

SCHEMA = types.FunctionDeclaration(
    name="web_search",
    description="인터넷에서 정보를 검색합니다. 최신 뉴스, 날씨, 실시간 정보 등을 찾을 때 사용합니다.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "query": types.Schema(type="STRING", description="검색할 키워드 또는 질문"),
            "max_results": types.Schema(type="INTEGER", description="가져올 결과 수 (기본값: 5)"),
        },
        required=["query"],
    ),
)

def main(query: str, max_results: int = 5) -> str:
    """DuckDuckGo를 사용하여 웹 검색을 수행합니다."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='kr-kr', max_results=max_results))
        
        if not results:
            return "검색 결과가 없습니다."
        
        # 결과 포맷팅
        formatted = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "제목 없음")
            url = r.get("href", "")
            body = r.get("body", "")[:200]  # 요약 200자 제한
            formatted.append(f"{i}. {title}\n   URL: {url}\n   {body}")
        
        return "\n\n".join(formatted)
        
    except Exception as e:
        return f"검색 오류: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(main(" ".join(sys.argv[1:])))
    else:
        print(SCHEMA.model_dump_json(indent=2))

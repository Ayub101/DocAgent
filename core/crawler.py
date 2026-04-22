import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl_url(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        markdown = getattr(result, "markdown", None)
        if markdown and markdown.strip():
            return markdown.strip()

        text = getattr(result, "text", "") or ""
        html = getattr(result, "html", "") or ""
        return (text.strip() or html.strip())

def crawl_url_sync(url: str) -> str:
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return asyncio.get_event_loop().run_until_complete(crawl_url(url))
    except RuntimeError:
        pass

    return asyncio.run(crawl_url(url))
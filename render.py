"""Render build.html to entry.png (1024x1024) with Playwright, and print
measurements plus the PNG sha256. Run from the repo dir. The page is static
local HTML/CSS/SVG, so repeated renders produce identical PNG bytes."""
import asyncio
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parent


async def main():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1024, "height": 1024})
        await pg.goto(f"file://{REPO}/build.html")
        await pg.wait_for_timeout(400)
        m = await pg.evaluate("""() => {
          const foot = document.querySelector('.foot');
          const r = foot.getBoundingClientRect();
          const page = document.querySelector('.page');
          return {footBottom: r.bottom, pageH: page.getBoundingClientRect().height,
                  bodyScrollH: document.body.scrollHeight,
                  overflow: document.body.scrollHeight > 1024};
        }""")
        print("measure:", m)
        await pg.screenshot(path=str(REPO / "entry.png"))
        await b.close()
    data = (REPO / "entry.png").read_bytes()
    print("bytes:", len(data))
    print("sha256:", hashlib.sha256(data).hexdigest())


asyncio.run(main())

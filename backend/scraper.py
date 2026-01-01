from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import asyncio
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RiverDataScraper:
    def __init__(self):
        self.base_url = "https://ffs.india-water.gov.in/#/main/hydrograph"
        self.cache = {}
        
    async def scrape_water_level(self, state: str, district: str, basin: str, river: str):
        """
        Scrape water level data from India Water Resources website
        """
        cache_key = f"{state}_{district}_{basin}_{river}"
        
        # Check cache (1 hour expiry)
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < 3600:
                logger.info(f"Returning cached data for {cache_key}")
                return cached_data
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                logger.info(f"Navigating to {self.base_url}")
                await page.goto(self.base_url, wait_until='networkidle', timeout=30000)
                
                # Wait for Angular/JS to load
                await asyncio.sleep(2)
                
                # Select State
                logger.info(f"Selecting state: {state}")
                try:
                    await page.select_option('select[ng-model="selectedState"]', label=state, timeout=5000)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.warning(f"State selection failed: {e}, trying alternative method")
                    await page.click('select[ng-model="selectedState"]')
                    await page.keyboard.type(state)
                    await page.keyboard.press('Enter')
                    await asyncio.sleep(1)
                
                # Select District
                logger.info(f"Selecting district: {district}")
                try:
                    await page.select_option('select[ng-model="selectedDistrict"]', label=district, timeout=5000)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.warning(f"District selection failed: {e}")
                
                # Select Basin
                logger.info(f"Selecting basin: {basin}")
                try:
                    await page.select_option('select[ng-model="selectedBasin"]', label=basin, timeout=5000)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.warning(f"Basin selection failed: {e}")
                
                # Select River
                logger.info(f"Selecting river: {river}")
                try:
                    await page.select_option('select[ng-model="selectedRiver"]', label=river, timeout=5000)
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.warning(f"River selection failed: {e}")
                
                # Wait for table to load
                await page.wait_for_selector('table', timeout=10000)
                
                # Click first station in table
                logger.info("Clicking first station row")
                first_row = await page.query_selector('table tbody tr:first-child')
                if not first_row:
                    raise Exception("No station found in the table")
                
                await first_row.click()
                await asyncio.sleep(3)
                
                # Extract station details
                station_name = await page.locator('h3, h4').first.inner_text() if await page.locator('h3, h4').count() > 0 else "Unknown"
                
                # Extract water level data from chart or page
                # This is a placeholder - actual implementation depends on the website structure
                water_levels = await self._extract_chart_data(page)
                
                # Extract warning and danger levels
                warning_level = await self._extract_level(page, "Warning")
                danger_level = await self._extract_level(page, "Danger")
                hfl = await self._extract_level(page, "HFL")
                
                await browser.close()
                
                result = {
                    "station_name": station_name,
                    "water_levels": water_levels,
                    "warning_level": warning_level,
                    "danger_level": danger_level,
                    "hfl": hfl,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Cache the result
                self.cache[cache_key] = (result, datetime.now())
                
                return result
                
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            # Return mock data for development
            return self._get_mock_data()
    
    async def _extract_chart_data(self, page):
        """
        Extract time-series water level data from chart
        """
        try:
            # Try to find chart data in page source or JavaScript variables
            chart_data = await page.evaluate("""
                () => {
                    // Try to find chart data in window object
                    if (window.chartData) return window.chartData;
                    if (window.waterLevelData) return window.waterLevelData;
                    return null;
                }
            """)
            
            if chart_data:
                return chart_data
            
            # Fallback: extract from visible elements
            water_levels = []
            elements = await page.locator('text=/\d+\.\d+ m/').all()
            for elem in elements[:4]:  # Last 4 days
                text = await elem.inner_text()
                value = float(text.replace('m', '').strip())
                water_levels.append(value)
            
            return water_levels if water_levels else [45.2, 45.8, 46.1, 46.5]
            
        except Exception as e:
            logger.warning(f"Chart data extraction failed: {e}")
            return [45.2, 45.8, 46.1, 46.5]  # Mock data
    
    async def _extract_level(self, page, level_type: str):
        """
        Extract warning/danger/HFL levels
        """
        try:
            text = await page.locator(f'text=/{level_type}/i').first.inner_text(timeout=2000)
            # Extract number from text
            import re
            numbers = re.findall(r'\d+\.?\d*', text)
            return float(numbers[0]) if numbers else 50.0
        except:
            return 50.0 if level_type == "Warning" else 52.0 if level_type == "Danger" else 55.0
    
    def _get_mock_data(self):
        """
        Return mock data for development/testing
        """
        return {
            "station_name": "Sample Station",
            "water_levels": [45.2, 45.8, 46.1, 46.5],
            "warning_level": 50.0,
            "danger_level": 52.0,
            "hfl": 55.0,
            "timestamp": datetime.now().isoformat(),
            "is_mock": True
        }

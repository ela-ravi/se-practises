import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def login_to_hrone(username, password):
    async with async_playwright() as p:
        # Launch browser (visible mode)
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # Navigate to login page
            print("Navigating to HR One login page...")
            await page.goto('https://app.hrone.cloud/login', wait_until='networkidle')
            
            # Enter username and click continue
            print("Entering username...")
            await page.fill('#hrone-username', username)
            print("Clicking Next...")
            await page.click('//*[@id="login-register"]/div/div[1]/div[2]/button')
            
            # Wait for password field to be visible
            print("Waiting for password field...")
            password_field = await page.wait_for_selector('#hrone-password', state='visible', timeout=10000)
            
            # Enter password
            print("Entering password...")
            await password_field.fill(password)
            
            # Click the login button on password page
            print("Clicking login button...")
            login_button = await page.wait_for_selector('//*[@id="login-register"]/div/div[3]/div[3]/button[2]', state='visible', timeout=10000)
            await login_button.click()
            
            # Wait for navigation to complete and dashboard to load
            print("Waiting for dashboard to load...")
            try:
                # Wait for the dashboard header to be visible
                dashboard_header = await page.wait_for_selector(
                    'xpath=/html/body/app-root/app-main-dashboard/app-main/div/app-header/header/nav',
                    state='visible',
                    timeout=15000  # 15 seconds timeout
                )
                print("✅ Dashboard loaded successfully!")
                
                # Add a small delay to ensure any modals have time to appear
                await asyncio.sleep(2)
                
                # Check for modal and close it if visible
                try:
                    print("Checking for modal...")
                    modal = await page.query_selector('xpath=/html/body/div[2]/div')
                    if modal and await modal.is_visible():
                        print("Modal detected. Attempting to close...")
                        close_button = await page.wait_for_selector(
                            'xpath=/html/body/div[2]/div/div[3]/div/button', 
                            state='visible', 
                            timeout=5000
                        )
                        await close_button.click()
                        print("✅ Modal closed successfully")
                    else:
                        print("No modal found")
                    
                    # Click the Mark Attendance button
                    print("Clicking Mark Attendance button...")
                    mark_attendance_btn = await page.wait_for_selector(
                        'xpath=//*[@id="headerTopContent"]/div[2]/div[1]/div[2]/div/button',
                        state='visible',
                        timeout=10000
                    )
                    await mark_attendance_btn.click()
                    print("✅ Mark Attendance button clicked successfully!")

                    # Wait for attendance dialog to appear
                    print("Waiting for attendance dialog...")
                    attendance_dialog = await page.wait_for_selector(
                        'xpath=/html/body/div[2]/div/div[3]/div',
                        state='visible',
                        timeout=10000
                    )
                    print("✅ Attendance dialog appeared")

                    # Click the final Mark Attendance button in the dialog
                    print("Clicking final Mark Attendance button in dialog...")
                    final_mark_btn = await page.wait_for_selector(
                        'xpath=/html/body/div[2]/div/div[3]/div/div[2]/div/div/div[2]/button[2]',
                        state='visible',
                        timeout=10000
                    )
                    await final_mark_btn.click()
                    print("✅ Final Mark Attendance button clicked successfully!")
                    
                    # # Wait for the network request to complete and check response
                    # print("Waiting for attendance request to complete...")
                    
                    # try:
                    #     # Wait for the API response with a timeout
                    #     response = await page.wait_for_response(
                    #         lambda response: "timeoffice/mobile/checkin/Attendance/Request" in response.url,
                    #         timeout=15000  # 15 seconds timeout
                    #     )
                        
                    #     try:
                    #         response_data = await response.json()
                    #         if response_data.get("message") == "Record saved successfully.":
                    #             print("✅ Success: Record saved successfully!")
                    #             print(f"Response: {response_data}")
                    #         else:
                    #             error_msg = response_data.get("message", "Unknown error occurred")
                    #             print(f"❌ Error: {error_msg}")
                    #             await page.screenshot(path='attendance_error.png')
                    #             print("Screenshot saved as attendance_error.png")
                    #     except Exception as e:
                    #         print(f"❌ Error parsing response: {str(e)}")
                    #         await page.screenshot(path='attendance_error.png')
                    #         print("Screenshot saved as attendance_error.png")
                            
                    # except Exception as e:
                    #     print(f"❌ Error waiting for attendance response: {str(e)}")
                    #     await page.screenshot(path='attendance_timeout.png')
                    #     print("Screenshot saved as attendance_timeout.png")
                    
                except Exception as modal_error:
                    print(f"❌ Error during attendance process: {str(modal_error)}")
                    await page.screenshot(path='attendance_error.png')
                    print("Screenshot saved as attendance_error.png")
                    # Keep browser open for inspection
                    await page.pause()
                    raise
                    
            except Exception as e:
                print(f"❌ Error waiting for dashboard: {str(e)}")
                await page.screenshot(path='dashboard_error.png')
                print("Screenshot saved as dashboard_error.png")
                # Keep browser open for inspection
                await page.pause()
                raise
            
            # After all operations are complete
            print("✅ All operations completed successfully!")
            print("Waiting for 3 seconds before closing...")
            await asyncio.sleep(3)
            await browser.close()
            print("✅ Browser closed.")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Take screenshot on error
            await page.screenshot(path='login_error.png')
            print("Screenshot saved as login_error.png")
        
        finally:
            # Close browser
            await browser.close()

def main():
    # Set credentials
    username = os.getenv('HRONE_USERNAME')
    password = os.getenv('HRONE_PASSWORD')
    
    if not username or not password:
        print("Error: Both username and password are required")
        return
    
    print("Starting HR One login automation with Playwright...")
    asyncio.run(login_to_hrone(username, password))

if __name__ == "__main__":
    main()

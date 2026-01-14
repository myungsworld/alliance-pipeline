# webdriver_mask.py - WebDriver 속성 숨김
# navigator.webdriver 등 탐지 포인트 제거

from typing import Any


def mask_webdriver_properties(driver: Any) -> None:
    """
    WebDriver 탐지 속성들을 숨김

    주요 탐지 포인트:
    - navigator.webdriver
    - window.chrome
    - permissions query

    undetected-chromedriver가 기본적으로 처리하지만
    추가적인 마스킹 적용
    """

    # navigator.webdriver 숨기기
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                // navigator.webdriver 제거
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });

                // chrome runtime 위장
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {},
                };

                // permissions query 위장
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );

                // plugins 위장 (빈 배열이면 봇으로 의심)
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf"},
                            description: "",
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        }
                    ],
                });

                // languages 위장
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['ko-KR', 'ko', 'en-US', 'en'],
                });
            """
        }
    )


def mask_automation_extensions(driver: Any) -> None:
    """자동화 관련 확장 프로그램 흔적 제거"""

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                // 자동화 확장 프로그램 ID 숨기기
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
        }
    )

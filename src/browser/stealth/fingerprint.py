# fingerprint.py - 브라우저 fingerprint 위장
# canvas, webgl, audio 등 fingerprint 요소 조작

import random
from typing import Any


def apply_fingerprint_mask(driver: Any) -> None:
    """
    브라우저 fingerprint 위장

    사이트들이 사용하는 fingerprint 수집 방법들:
    - Canvas fingerprint: canvas 렌더링 결과로 식별
    - WebGL fingerprint: GPU 정보로 식별
    - Audio fingerprint: 오디오 처리 결과로 식별
    - Font fingerprint: 설치된 폰트 목록으로 식별

    이런 값들에 미세한 노이즈를 추가하여 매번 다른 fingerprint 생성
    """

    # 노이즈 시드 (세션마다 다르게)
    noise_seed = random.random()

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": f"""
                // Canvas fingerprint 노이즈
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function(type) {{
                    if (type === 'image/png' && this.width > 16 && this.height > 16) {{
                        const context = this.getContext('2d');
                        if (context) {{
                            const imageData = context.getImageData(0, 0, this.width, this.height);
                            const data = imageData.data;

                            // 랜덤 픽셀에 미세한 노이즈 추가
                            for (let i = 0; i < data.length; i += 4) {{
                                if (Math.random() < 0.001) {{
                                    data[i] = (data[i] + Math.floor(Math.random() * 3) - 1) % 256;
                                }}
                            }}

                            context.putImageData(imageData, 0, 0);
                        }}
                    }}
                    return originalToDataURL.apply(this, arguments);
                }};

                // WebGL fingerprint 노이즈
                const getParameterProxyHandler = {{
                    apply: function(target, thisArg, argumentsList) {{
                        const param = argumentsList[0];
                        const result = Reflect.apply(target, thisArg, argumentsList);

                        // 렌더러/벤더 정보 약간 수정
                        if (param === 37445) {{ // UNMASKED_VENDOR_WEBGL
                            return result + ' ';
                        }}
                        if (param === 37446) {{ // UNMASKED_RENDERER_WEBGL
                            return result + ' ';
                        }}

                        return result;
                    }}
                }};

                // WebGL 컨텍스트 프록시
                const originalGetContext = HTMLCanvasElement.prototype.getContext;
                HTMLCanvasElement.prototype.getContext = function(type, ...args) {{
                    const context = originalGetContext.apply(this, [type, ...args]);

                    if (context && (type === 'webgl' || type === 'webgl2')) {{
                        const originalGetParameter = context.getParameter.bind(context);
                        context.getParameter = new Proxy(originalGetParameter, getParameterProxyHandler);
                    }}

                    return context;
                }};

                // Audio fingerprint 노이즈
                const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
                AudioContext.prototype.createAnalyser = function() {{
                    const analyser = originalCreateAnalyser.apply(this, arguments);
                    const originalGetFloatFrequencyData = analyser.getFloatFrequencyData.bind(analyser);

                    analyser.getFloatFrequencyData = function(array) {{
                        originalGetFloatFrequencyData(array);
                        // 미세한 노이즈 추가
                        for (let i = 0; i < array.length; i++) {{
                            array[i] += (Math.random() - 0.5) * 0.0001;
                        }}
                    }};

                    return analyser;
                }};

                // 스크린 정보 약간의 변형
                const screenProps = {{
                    width: window.screen.width + (Math.floor(Math.random() * 2) - 1),
                    height: window.screen.height + (Math.floor(Math.random() * 2) - 1),
                    availWidth: window.screen.availWidth + (Math.floor(Math.random() * 2) - 1),
                    availHeight: window.screen.availHeight + (Math.floor(Math.random() * 2) - 1),
                }};

                // 읽기 전용 속성 수정 (일부 브라우저에서만 동작)
                try {{
                    Object.defineProperty(window.screen, 'width', {{ get: () => screenProps.width }});
                    Object.defineProperty(window.screen, 'height', {{ get: () => screenProps.height }});
                }} catch(e) {{}}
            """
        }
    )


def get_random_screen_resolution() -> tuple:
    """랜덤한 실제 사용되는 해상도 반환"""
    resolutions = [
        (1920, 1080),
        (1366, 768),
        (1536, 864),
        (1440, 900),
        (1280, 720),
        (2560, 1440),
    ]
    return random.choice(resolutions)

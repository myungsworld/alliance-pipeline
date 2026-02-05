// ============================================
// Express API 서버
// n8n에서 HTTP 요청으로 영상 렌더링 호출
// ============================================
import express from 'express';
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';
import { RenderRequest, RenderResponse } from '../types';

const app = express();
app.use(express.json());

// CORS 허용 (Remotion 렌더링용)
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Range');
  res.header('Access-Control-Expose-Headers', 'Content-Length, Content-Range');
  next();
});

// 미디어 파일 정적 제공 (/data/media/ -> http://localhost:3001/media/)
app.use('/media', express.static('/data/media'));

const PORT = process.env.PORT || 3001;

// 렌더링 엔드포인트
app.post('/render', async (req, res) => {
  const { compositionId, props, outputPath } = req.body as RenderRequest;

  console.log(`[Render] Starting: ${compositionId}`, props);

  try {
    // 1. Remotion 번들 생성
    console.log('[Render] Bundling...');
    const bundleLocation = await bundle({
      entryPoint: path.resolve(__dirname, '../index.ts'),
      webpackOverride: (config) => config,
    });

    // 2. 컴포지션 선택
    console.log('[Render] Selecting composition...');
    const composition = await selectComposition({
      serveUrl: bundleLocation,
      id: compositionId,
      inputProps: props,
    });

    // 3. 영상 렌더링
    console.log('[Render] Rendering video...');
    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: outputPath,
      inputProps: props,
    });

    console.log(`[Render] Complete: ${outputPath}`);

    const response: RenderResponse = {
      success: true,
      outputPath,
    };
    res.json(response);

  } catch (error) {
    console.error('[Render] Error:', error);
    const response: RenderResponse = {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
    res.status(500).json(response);
  }
});

// 헬스체크
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(`Remotion render server running on port ${PORT}`);
});

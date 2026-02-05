// ============================================
// 미디어 렌더러 컴포넌트
// 비디오/이미지를 트랜지션 효과와 함께 렌더링
// ============================================
import { OffthreadVideo, Img } from 'remotion';
import { MediaItem, TransitionType } from '../../types';
import { getTransitionStyle } from './transitions';

interface MediaRendererProps {
  item: MediaItem;
  transitionProgress: number;
  transitionType: TransitionType;
  isTransitionOut: boolean;
}

// /data/media/xxx -> http://localhost:3001/media/xxx
const resolveSrc = (src: string): string => {
  if (src.startsWith('/data/media/')) {
    return `http://localhost:3001${src.replace('/data/media/', '/media/')}`;
  }
  return src;
};

export const MediaRenderer: React.FC<MediaRendererProps> = ({
  item,
  transitionProgress,
  transitionType,
  isTransitionOut,
}) => {
  const { opacity, transform } = getTransitionStyle(
    transitionProgress,
    transitionType,
    isTransitionOut
  );

  const style: React.CSSProperties = {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    opacity,
    transform,
  };

  const src = resolveSrc(item.src);

  if (item.type === 'video') {
    return <OffthreadVideo src={src} style={style} />;
  }
  return <Img src={src} style={style} />;
};

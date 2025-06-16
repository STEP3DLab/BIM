import { useEffect, useRef } from 'react';
import Potree from 'potree-core';

interface ViewerPageProps {
  url: string;
}

export default function ViewerPage({ url }: ViewerPageProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const viewer = new Potree.Viewer(containerRef.current);
    viewer.setEDLEnabled(true);
    viewer.loadPointCloud(url, 'cloud');
  }, [url]);

  return <div style={{ height: '100vh' }} ref={containerRef} />;
}

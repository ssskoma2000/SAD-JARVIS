'use client';

import Spline from '@splinetool/react-spline';

export default function SplineScene() {
  return (
    <div className="absolute top-0 left-0 w-full h-full z-0">
      <Spline scene="https://prod.spline.design/6Wq1Q7Y3FjI-2wZt/scene.splinecode" />
    </div>
  );
}

'use client';

export default function Hero() {
  return (
    <section className="min-h-[600px] bg-base-100 px-4 py-16">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-6xl md:text-7xl lg:text-8xl mb-6 tracking-tight text-base-content">
          Curated for the<br />modern minimalist
        </h1>
        <p className="text-xl mb-8 max-w-xl text-base-content/60">
          Discover our collection of timeless products designed with intention and
          crafted with care.
        </p>
        <button className="btn btn-primary btn-lg group">
          Explore Collection
          <span className="text-xl inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
        </button>
      </div>
    </section>
  );
}


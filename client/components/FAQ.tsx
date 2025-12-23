import type { FAQ } from '@/types/faq';

interface FAQProps {
  faqs: FAQ[];
}

export default function FAQ({ faqs }: FAQProps) {
  // Don't render if no FAQs provided
  if (!faqs || faqs.length === 0) {
    return null;
  }

  return (
    <section className="min-h-[400px] bg-base-100 py-16">
      <div className="max-w-7xl mx-auto px-8 md:px-4">
        <h2 className="text-4xl md:text-5xl font-semibold text-base-content uppercase tracking-tight mb-12">
          FAQ
        </h2>
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <details
              key={index}
              className="collapse collapse-arrow bg-base-200 border border-base-300"
            >
              <summary className="collapse-title text-base-content font-medium text-lg">
                {faq.title}
              </summary>
              <div className="collapse-content">
                <p className="text-base-content/80">{faq.content}</p>
              </div>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}



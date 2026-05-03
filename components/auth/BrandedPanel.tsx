import { Shield, TrendingUp, Zap, CheckCircle } from 'lucide-react';

export default function BrandedPanel() {
  const features = [
    {
      icon: <Shield size={24} />,
      title: 'AI-Powered Assessment',
      description: 'Computer vision and geospatial analysis for accurate credit scoring',
    },
    {
      icon: <TrendingUp size={24} />,
      title: 'Real-Time Insights',
      description: 'Instant CSQS scores and cash flow estimates for faster decisions',
    },
    {
      icon: <Zap size={24} />,
      title: 'Streamlined Workflow',
      description: 'From image upload to approval in under 60 seconds',
    },
  ];

  return (
    <div className="hidden lg:flex lg:w-3/5 bg-primary text-white p-12 flex-col justify-between relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
      
      <div className="relative z-10">
        {/* Logo */}
        <div className="flex items-center gap-3 mb-12">
          <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center">
            <span className="text-white font-heading font-bold text-xl">KL</span>
          </div>
          <div>
            <h1 className="text-2xl font-heading font-bold">KiranaLens</h1>
            <p className="text-white/70 text-sm">AI Underwriting Platform</p>
          </div>
        </div>

        {/* Tagline */}
        <div className="mb-12">
          <h2 className="text-4xl font-heading font-bold mb-4 leading-tight">
            Credit intelligence<br />for India&apos;s kirana economy
          </h2>
          <p className="text-white/80 text-lg">
            Empowering NBFCs with AI-driven underwriting for neighborhood retail stores
          </p>
        </div>

        {/* Features */}
        <div className="space-y-6">
          {features.map((feature, index) => (
            <div key={index} className="flex items-start gap-4">
              <div className="flex-shrink-0 w-12 h-12 bg-accent/20 rounded-lg flex items-center justify-center text-accent">
                {feature.icon}
              </div>
              <div>
                <h3 className="font-heading font-semibold text-lg mb-1">{feature.title}</h3>
                <p className="text-white/70 text-sm">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="relative z-10 flex items-center gap-2 text-white/60 text-sm">
        <CheckCircle size={16} />
        <span>Trusted by leading NBFCs across India</span>
      </div>
    </div>
  );
}

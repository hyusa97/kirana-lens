import { ReactNode } from 'react';

interface PageWrapperProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

export default function PageWrapper({ children, title, description }: PageWrapperProps) {
  return (
    <div className="p-6">
      {(title || description) && (
        <div className="mb-6">
          {title && <h1 className="text-3xl font-heading font-bold text-primary mb-2">{title}</h1>}
          {description && <p className="text-gray-600">{description}</p>}
        </div>
      )}
      {children}
    </div>
  );
}

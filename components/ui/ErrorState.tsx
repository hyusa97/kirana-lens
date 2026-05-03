import { AlertTriangle, RefreshCw, Wifi, WifiOff } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  type?: 'network' | 'server' | 'validation' | 'generic';
  onRetry?: () => void;
  showRetry?: boolean;
}

export default function ErrorState({
  title,
  message,
  type = 'generic',
  onRetry,
  showRetry = true,
}: ErrorStateProps) {
  const getErrorConfig = () => {
    switch (type) {
      case 'network':
        return {
          icon: WifiOff,
          defaultTitle: 'Connection Error',
          defaultMessage: 'Unable to connect to the server. Please check your internet connection and try again.',
          color: 'text-orange-500',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200',
        };
      case 'server':
        return {
          icon: AlertTriangle,
          defaultTitle: 'Server Error',
          defaultMessage: 'Something went wrong on our end. Please try again in a few moments.',
          color: 'text-red-500',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
        };
      case 'validation':
        return {
          icon: AlertTriangle,
          defaultTitle: 'Validation Error',
          defaultMessage: 'Please check your input and try again.',
          color: 'text-yellow-500',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
        };
      default:
        return {
          icon: AlertTriangle,
          defaultTitle: 'Something went wrong',
          defaultMessage: 'An unexpected error occurred. Please try again.',
          color: 'text-gray-500',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200',
        };
    }
  };

  const config = getErrorConfig();
  const Icon = config.icon;

  return (
    <div className={`${config.bgColor} ${config.borderColor} border rounded-card p-8 text-center`}>
      <div className={`inline-flex items-center justify-center w-16 h-16 ${config.bgColor} rounded-full mb-4`}>
        <Icon size={32} className={config.color} />
      </div>
      
      <h3 className="text-lg font-heading font-semibold text-gray-900 mb-2">
        {title || config.defaultTitle}
      </h3>
      
      <p className="text-gray-600 mb-6 max-w-md mx-auto">
        {message || config.defaultMessage}
      </p>
      
      {showRetry && onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 bg-accent hover:bg-accent/90 text-white rounded-input font-medium transition-colors"
        >
          <RefreshCw size={16} />
          Try Again
        </button>
      )}
    </div>
  );
}
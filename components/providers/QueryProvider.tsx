'use client';

import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/queryClient';
import { ReactNode, useEffect } from 'react';
import { USE_MOCK_BACKEND } from '@/lib/apiClient';
import { setupMockInterceptor } from '@/lib/mockInterceptor';

export function QueryProvider({ children }: { children: ReactNode }) {
  // Setup mock interceptor if using mock backend
  useEffect(() => {
    if (USE_MOCK_BACKEND) {
      console.log('🔧 Using mock backend - no real API required');
      setupMockInterceptor();
    }
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

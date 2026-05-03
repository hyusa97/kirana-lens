'use client';

import { usePathname } from 'next/navigation';
import { ChevronRight } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

const routeLabels: Record<string, string> = {
  dashboard: 'Dashboard',
  assess: 'New Assessment',
  admin: 'All Assessments',
  processing: 'Processing',
};

export default function TopBar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const segments = pathname.split('/').filter(Boolean);

  const breadcrumbs = segments.map((segment, index) => {
    const label = routeLabels[segment] || segment;
    const href = '/' + segments.slice(0, index + 1).join('/');
    return { label, href, isLast: index === segments.length - 1 };
  });

  // Get initials from name
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Breadcrumbs */}
        <div className="flex items-center gap-2 text-sm">
          {breadcrumbs.map((crumb, index) => (
            <div key={crumb.href} className="flex items-center gap-2">
              {index > 0 && <ChevronRight size={16} className="text-gray-400" />}
              <span
                className={
                  crumb.isLast
                    ? 'text-primary font-medium'
                    : 'text-gray-600 hover:text-primary cursor-pointer'
                }
              >
                {crumb.label}
              </span>
            </div>
          ))}
        </div>

        {/* User info */}
        {user && (
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">{user.name}</p>
              <p className="text-xs text-gray-500 capitalize">{user.role.replace('_', ' ')}</p>
            </div>
            <div className="w-10 h-10 bg-accent rounded-full flex items-center justify-center text-white font-heading font-semibold">
              {getInitials(user.name)}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}

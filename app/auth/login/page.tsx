'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Loader2, TestTube } from 'lucide-react';
import toast from 'react-hot-toast';
import BrandedPanel from '@/components/auth/BrandedPanel';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/lib/services/api';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  rememberMe: z.boolean().optional(),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { setUser, setTokens } = useAuthStore();

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    
    try {
      const response = await authApi.login({
        email: data.email,
        password: data.password,
      });
      
      // Handle both real API (camelCase) and mock API (snake_case) formats
      const authResponse = response as any;
      const token = authResponse.accessToken || authResponse.access_token;
      const refToken = authResponse.refreshToken || authResponse.refresh_token;
      
      setUser(response.user);
      setTokens(token, refToken);
      
      toast.success(`Welcome back, ${response.user.name}!`);
      
      // Navigate to dashboard
      router.push('/dashboard');
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Invalid email or password';
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const fillDemoCredentials = () => {
    setValue('email', 'demo@kiranalens.com');
    setValue('password', 'Demo@1234');
    toast.success('Demo credentials filled!');
  };

  return (
    <div className="flex min-h-screen">
      <BrandedPanel />
      
      {/* Right side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-card shadow-2xl p-8">
            {/* Header */}
            <div className="mb-8">
              <h2 className="text-3xl font-heading font-bold text-primary mb-2">
                Sign in to KiranaLens
              </h2>
              <p className="text-gray-600">
                Enter your credentials to access your account
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  {...register('email')}
                  type="email"
                  id="email"
                  placeholder="you@nbfc.com"
                  className={`w-full px-4 py-3 border rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent ${
                    errors.email ? 'border-danger' : 'border-gray-300'
                  }`}
                />
                {errors.email && (
                  <p className="mt-1 text-sm text-danger">{errors.email.message}</p>
                )}
              </div>

              {/* Password */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <input
                    {...register('password')}
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    placeholder="Enter your password"
                    className={`w-full px-4 py-3 border rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent pr-12 ${
                      errors.password ? 'border-danger' : 'border-gray-300'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
                {errors.password && (
                  <p className="mt-1 text-sm text-danger">{errors.password.message}</p>
                )}
              </div>

              {/* Remember Me */}
              <div className="flex items-center justify-between">
                <label className="flex items-center">
                  <input
                    {...register('rememberMe')}
                    type="checkbox"
                    className="rounded border-gray-300 text-accent focus:ring-accent"
                  />
                  <span className="ml-2 text-sm text-gray-600">Remember me</span>
                </label>
                <Link href="#" className="text-sm text-accent hover:text-accent/80">
                  Forgot password?
                </Link>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-accent hover:bg-accent/90 text-white py-3 rounded-input font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    Signing in...
                  </>
                ) : (
                  'Sign in'
                )}
              </button>
            </form>

            {/* Register Link */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Don&apos;t have an account?{' '}
                <Link href="/auth/register" className="text-accent hover:text-accent/80 font-medium">
                  Register here
                </Link>
              </p>
            </div>
          </div>

          {/* Footer */}
          <p className="mt-8 text-center text-sm text-gray-400">
            © 2026 KiranaLens. All rights reserved.
          </p>
        </div>
      </div>

      {/* Demo Mode Toggle - Only in development */}
      {process.env.NODE_ENV === 'development' && (
        <button
          onClick={fillDemoCredentials}
          className="fixed bottom-4 left-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 text-sm font-medium transition-colors z-50"
          title="Fill demo credentials for testing"
        >
          <TestTube size={16} />
          Demo Mode
        </button>
      )}
    </div>
  );
}

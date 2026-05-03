'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import BrandedPanel from '@/components/auth/BrandedPanel';
import PasswordStrength from '@/components/auth/PasswordStrength';
import authService from '@/lib/services/authService';

const registerSchema = z.object({
  fullName: z.string().min(2, 'Full name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  organization: z.string().min(2, 'Organization name is required'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string(),
  role: z.enum(['credit_officer', 'branch_manager', 'admin']).refine((val) => !!val, {
    message: 'Please select a role',
  }),
  agreeToTerms: z.boolean().refine((val) => val === true, {
    message: 'You must agree to the Terms of Service',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    
    try {
      await authService.register({
        name: data.fullName,
        email: data.email,
        organization: data.organization,
        password: data.password,
        role: data.role as 'analyst' | 'manager' | 'admin',
      });
      
      toast.success('Account created successfully! Please sign in.');
      router.push('/auth/login');
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      <BrandedPanel />
      
      {/* Right side - Register Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-card shadow-2xl p-8">
            {/* Header */}
            <div className="mb-8">
              <h2 className="text-3xl font-heading font-bold text-primary mb-2">
                Create your account
              </h2>
              <p className="text-gray-600">
                Join KiranaLens to start underwriting
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
              {/* Full Name */}
              <div>
                <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <input
                  {...register('fullName')}
                  type="text"
                  id="fullName"
                  placeholder="Priya Sharma"
                  className={`w-full px-4 py-3 border rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent ${
                    errors.fullName ? 'border-danger' : 'border-gray-300'
                  }`}
                />
                {errors.fullName && (
                  <p className="mt-1 text-sm text-danger">{errors.fullName.message}</p>
                )}
              </div>

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

              {/* Organization */}
              <div>
                <label htmlFor="organization" className="block text-sm font-medium text-gray-700 mb-2">
                  Organisation / NBFC Name
                </label>
                <input
                  {...register('organization')}
                  type="text"
                  id="organization"
                  placeholder="ABC Finance Ltd."
                  className={`w-full px-4 py-3 border rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent ${
                    errors.organization ? 'border-danger' : 'border-gray-300'
                  }`}
                />
                {errors.organization && (
                  <p className="mt-1 text-sm text-danger">{errors.organization.message}</p>
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
                    placeholder="Create a strong password"
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
                <PasswordStrength password={password || ''} />
                {errors.password && (
                  <p className="mt-1 text-sm text-danger">{errors.password.message}</p>
                )}
              </div>

              {/* Confirm Password */}
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <input
                    {...register('confirmPassword')}
                    type={showConfirmPassword ? 'text' : 'password'}
                    id="confirmPassword"
                    placeholder="Re-enter your password"
                    className={`w-full px-4 py-3 border rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent pr-12 ${
                      errors.confirmPassword ? 'border-danger' : 'border-gray-300'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-danger">{errors.confirmPassword.message}</p>
                )}
              </div>

              {/* Role */}
              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                  Role
                </label>
                <select
                  {...register('role')}
                  id="role"
                  className={`w-full px-4 py-3 border rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent ${
                    errors.role ? 'border-danger' : 'border-gray-300'
                  }`}
                >
                  <option value="">Select your role</option>
                  <option value="credit_officer">Credit Officer</option>
                  <option value="branch_manager">Branch Manager</option>
                  <option value="admin">Admin</option>
                </select>
                {errors.role && (
                  <p className="mt-1 text-sm text-danger">{errors.role.message}</p>
                )}
              </div>

              {/* Terms Checkbox */}
              <div>
                <label className="flex items-start">
                  <input
                    {...register('agreeToTerms')}
                    type="checkbox"
                    className="mt-1 rounded border-gray-300 text-accent focus:ring-accent"
                  />
                  <span className="ml-2 text-sm text-gray-600">
                    I agree to the{' '}
                    <Link href="#" className="text-accent hover:text-accent/80">
                      Terms of Service
                    </Link>{' '}
                    and{' '}
                    <Link href="#" className="text-accent hover:text-accent/80">
                      Privacy Policy
                    </Link>
                  </span>
                </label>
                {errors.agreeToTerms && (
                  <p className="mt-1 text-sm text-danger">{errors.agreeToTerms.message}</p>
                )}
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
                    Creating account...
                  </>
                ) : (
                  'Create account'
                )}
              </button>
            </form>

            {/* Login Link */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Already have an account?{' '}
                <Link href="/auth/login" className="text-accent hover:text-accent/80 font-medium">
                  Sign in here
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
    </div>
  );
}

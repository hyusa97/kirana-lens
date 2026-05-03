'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, ArrowRight, CheckCircle, Loader2 } from 'lucide-react';
import PageWrapper from '@/components/layout/PageWrapper';
import StepIndicator from '@/components/assess/StepIndicator';
import ImageUploadZone from '@/components/ui/ImageUploadZone';
import GpsCapture from '@/components/ui/GpsCapture';
import { useCreateAssessment } from '@/hooks/useAssessments';
import toast from 'react-hot-toast';

const STEPS = ['Upload Images', 'Capture Location', 'Confirmation'];

export default function AssessPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [formData, setFormData] = useState({
    images: [] as File[],
    lat: 0,
    lng: 0,
    storeName: '',
    notes: '',
    gpsAccuracy: 0,
  });

  const createAssessment = useCreateAssessment();

  const handleNext = () => {
    if (currentStep === 1 && formData.images.length < 3) {
      toast.error('Please upload at least 3 images');
      return;
    }
    if (currentStep === 2 && formData.lat === 0) {
      toast.error('Please capture GPS location');
      return;
    }
    setCurrentStep(currentStep + 1);
  };

  const handleBack = () => {
    setCurrentStep(currentStep - 1);
  };

  const handleSubmit = () => {
    createAssessment.mutate({
      images: formData.images,
      lat: formData.lat,
      lng: formData.lng,
      store_name: formData.storeName || undefined,
      gps_accuracy: formData.gpsAccuracy || undefined,
      notes: formData.notes || undefined,
      onUploadProgress: (progress) => {
        setUploadProgress(progress);
      },
    });
  };

  return (
    <PageWrapper
      title="New Assessment"
      description="Upload store images and capture location to generate AI-powered insights"
    >
      <div className="max-w-4xl mx-auto">
        <StepIndicator currentStep={currentStep} steps={STEPS} />

        {/* Step 1: Upload Images */}
        {currentStep === 1 && (
          <div className="bg-white rounded-card border border-gray-200 p-8">
            <h2 className="text-2xl font-heading font-bold text-primary mb-2">
              Upload Store Images
            </h2>
            <p className="text-gray-600 mb-6">
              Upload clear, well-lit images of the store. Minimum 3 images required.
            </p>

            <ImageUploadZone
              onImagesChange={(files) => setFormData({ ...formData, images: files })}
              maxFiles={5}
              minFiles={3}
            />

            <div className="mt-8 flex justify-end">
              <button
                onClick={handleNext}
                disabled={formData.images.length < 3}
                className="bg-accent hover:bg-accent/90 text-white px-8 py-3 rounded-input font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                Next
                <ArrowRight size={20} />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Capture Location */}
        {currentStep === 2 && (
          <div className="bg-white rounded-card border border-gray-200 p-8">
            <h2 className="text-2xl font-heading font-bold text-primary mb-2">
              Capture Store Location
            </h2>
            <p className="text-gray-600 mb-6">
              Use GPS to capture the exact location of the store for geo-spatial analysis.
            </p>

            <GpsCapture
              onLocationCapture={(lat, lng, accuracy) => setFormData({ ...formData, lat, lng, gpsAccuracy: accuracy || 0 })}
            />

            {/* Optional Fields */}
            <div className="mt-8 space-y-4 border-t border-gray-200 pt-6">
              <div>
                <label htmlFor="storeName" className="block text-sm font-medium text-gray-700 mb-2">
                  Store Name (Optional)
                </label>
                <input
                  type="text"
                  id="storeName"
                  value={formData.storeName}
                  onChange={(e) => setFormData({ ...formData, storeName: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
                  placeholder="e.g., Sharma General Store"
                />
              </div>

              <div>
                <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-2">
                  Notes (Optional, max 200 characters)
                </label>
                <textarea
                  id="notes"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value.slice(0, 200) })}
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
                  placeholder="Any additional notes about the store..."
                />
                <p className="text-xs text-gray-500 mt-1">{formData.notes.length}/200 characters</p>
              </div>
            </div>

            <div className="mt-8 flex justify-between">
              <button
                onClick={handleBack}
                className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-8 py-3 rounded-input font-medium transition-colors flex items-center gap-2"
              >
                <ArrowLeft size={20} />
                Back
              </button>
              <button
                onClick={handleSubmit}
                disabled={formData.lat === 0 || createAssessment.isPending}
                className="bg-accent hover:bg-accent/90 text-white px-8 py-3 rounded-input font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {createAssessment.isPending ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    Uploading... {uploadProgress}%
                  </>
                ) : (
                  <>
                    Submit Assessment
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Confirmation */}
        {currentStep === 3 && (
          <div className="bg-white rounded-card border border-gray-200 p-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-success/10 rounded-full mb-4">
                <CheckCircle className="text-success" size={32} />
              </div>
              <h2 className="text-2xl font-heading font-bold text-primary mb-2">
                Assessment Submitted
              </h2>
              <p className="text-gray-600">
                Your assessment has been submitted successfully. Processing will begin shortly.
              </p>
            </div>

            {/* Summary */}
            <div className="bg-gray-50 rounded-card p-6 space-y-4">
              <h3 className="font-heading font-semibold text-primary mb-4">Submission Summary</h3>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-600">Images Uploaded</p>
                  <p className="font-medium text-gray-900">{formData.images.length} images</p>
                </div>
                <div>
                  <p className="text-gray-600">Location</p>
                  <p className="font-medium text-gray-900">
                    {formData.lat.toFixed(4)}, {formData.lng.toFixed(4)}
                  </p>
                </div>
                {formData.storeName && (
                  <div className="col-span-2">
                    <p className="text-gray-600">Store Name</p>
                    <p className="font-medium text-gray-900">{formData.storeName}</p>
                  </div>
                )}
                {formData.notes && (
                  <div className="col-span-2">
                    <p className="text-gray-600">Notes</p>
                    <p className="font-medium text-gray-900">{formData.notes}</p>
                  </div>
                )}
              </div>
            </div>

            <div className="mt-8 text-center">
              <p className="text-sm text-gray-600 mb-4">Redirecting to processing screen...</p>
              <div className="flex items-center justify-center gap-2">
                <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
      </div>
    </PageWrapper>
  );
}

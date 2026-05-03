'use client';

import { useState } from 'react';
import { MapPin, Loader2, CheckCircle } from 'lucide-react';

interface GpsCaptureProps {
  onLocationCapture: (lat: number, lng: number, accuracy?: number) => void;
}

export default function GpsCapture({ onLocationCapture }: GpsCaptureProps) {
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState<{ lat: number; lng: number; accuracy: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [manualAddress, setManualAddress] = useState('');
  const [useManual, setUseManual] = useState(false);

  const captureLocation = () => {
    setLoading(true);
    setError(null);

    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude, accuracy } = position.coords;
        setLocation({ lat: latitude, lng: longitude, accuracy });
        onLocationCapture(latitude, longitude, accuracy);
        setLoading(false);
      },
      (err) => {
        setError('Unable to retrieve location. Please enable location services or use manual address.');
        setLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  };

  return (
    <div className="space-y-6">
      {/* GPS Capture Button */}
      <div className="text-center">
        <button
          onClick={captureLocation}
          disabled={loading}
          className="inline-flex items-center gap-3 px-8 py-4 bg-accent text-white rounded-card hover:bg-accent/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-lg font-medium shadow-lg"
        >
          {loading ? (
            <>
              <Loader2 size={24} className="animate-spin" />
              <span>Capturing Location...</span>
            </>
          ) : (
            <>
              <MapPin size={24} />
              <span>Capture GPS Location</span>
            </>
          )}
        </button>
        <p className="text-sm text-gray-600 mt-3">
          Click to use your device&apos;s GPS for accurate location
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="text-sm text-danger bg-danger/10 border border-danger rounded-input p-4">
          <p className="font-medium mb-1">Location Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Location Captured */}
      {location && !useManual && (
        <div className="bg-success/10 border border-success rounded-card p-6">
          <div className="flex items-start gap-3 mb-4">
            <CheckCircle className="text-success flex-shrink-0 mt-1" size={24} />
            <div className="flex-1">
              <p className="text-lg font-medium text-success mb-2">Location Captured Successfully</p>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-600">Latitude</p>
                  <p className="font-mono font-medium text-gray-900">{location.lat.toFixed(6)}</p>
                </div>
                <div>
                  <p className="text-gray-600">Longitude</p>
                  <p className="font-mono font-medium text-gray-900">{location.lng.toFixed(6)}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-gray-600">Accuracy</p>
                  <p className="font-medium text-gray-900">{Math.round(location.accuracy)} metres</p>
                </div>
              </div>
            </div>
          </div>

          {/* Map Preview Placeholder */}
          <div className="h-48 bg-gray-200 rounded-input flex items-center justify-center overflow-hidden">
            <div className="text-center">
              <MapPin className="mx-auto text-gray-400 mb-2" size={32} />
              <p className="text-gray-600 text-sm">Map preview</p>
              <p className="text-gray-500 text-xs">
                {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Manual Address Override */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-gray-700">Manual Address Entry</h3>
          {!useManual && location && (
            <button
              onClick={() => setUseManual(true)}
              className="text-sm text-accent hover:text-accent/80 font-medium"
            >
              Use manual address instead
            </button>
          )}
        </div>
        
        {(useManual || !location) && (
          <div className="space-y-4">
            <textarea
              value={manualAddress}
              onChange={(e) => setManualAddress(e.target.value)}
              placeholder="Enter store address manually (e.g., Shop 12, MG Road, Bangalore, Karnataka 560001)"
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
            />
            {useManual && (
              <button
                onClick={() => setUseManual(false)}
                className="text-sm text-gray-600 hover:text-gray-900"
              >
                ← Back to GPS location
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

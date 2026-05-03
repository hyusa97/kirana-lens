import { create } from 'zustand';
import type { Assessment } from '@/lib/types';

interface AssessmentState {
  assessments: Assessment[];
  currentAssessment: Assessment | null;
  isLoading: boolean;
  setAssessments: (assessments: Assessment[]) => void;
  setCurrentAssessment: (assessment: Assessment | null) => void;
  setLoading: (isLoading: boolean) => void;
  addAssessment: (assessment: Assessment) => void;
  updateAssessment: (id: string, updates: Partial<Assessment>) => void;
}

export const useAssessmentStore = create<AssessmentState>((set) => ({
  assessments: [],
  currentAssessment: null,
  isLoading: false,
  
  setAssessments: (assessments) => set({ assessments }),
  
  setCurrentAssessment: (assessment) => set({ currentAssessment: assessment }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  addAssessment: (assessment) => set((state) => ({
    assessments: [assessment, ...state.assessments],
  })),
  
  updateAssessment: (id, updates) => set((state) => ({
    assessments: state.assessments.map((a) =>
      a.id === id ? { ...a, ...updates } : a
    ),
    currentAssessment:
      state.currentAssessment?.id === id
        ? { ...state.currentAssessment, ...updates }
        : state.currentAssessment,
  })),
}));

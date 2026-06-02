import { apiRequest, APIResponse } from "@/lib/apiClient";

export interface Resume {
  id: string;
  name: string;
  upload_status: string;
  created_at: string;
}

export interface OptimizeResponse {
  optimized_resume: string;
  ats_score: number;
  suggestions: string[];
}

export const resumeService = {
  /**
   * Uploads a resume document using multipart/form-data.
   */
  upload: async (
    file: File,
    resumeName: string
  ): Promise<APIResponse<{ resume_id: string; upload_status: string }>> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("resume_name", resumeName);

    // Let fetch determine Content-Type with multipart boundaries automatically
    return apiRequest<{ resume_id: string; upload_status: string }>("/resumes/upload", {
      method: "POST",
      body: formData,
    });
  },

  /**
   * Fetches list of all resumes belonging to the authenticated user.
   */
  getAll: async (): Promise<APIResponse<Resume[]>> => {
    return apiRequest<Resume[]>("/resumes", {
      method: "GET",
    });
  },

  /**
   * Fetches specific resume document text and parsing details.
   */
  getDetails: async (resumeId: string): Promise<APIResponse<any>> => {
    return apiRequest<any>(`/resumes/${resumeId}`, {
      method: "GET",
    });
  },

  /**
   * Triggers the AI optimization pipeline aligning the resume to a target role.
   */
  optimize: async (
    resumeId: string,
    targetRole: string
  ): Promise<APIResponse<OptimizeResponse>> => {
    return apiRequest<OptimizeResponse>("/ai/resume/optimize", {
      method: "POST",
      bodyData: { resume_id: resumeId, target_role: targetRole },
    });
  },
};

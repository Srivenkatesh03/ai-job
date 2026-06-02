import { apiRequest, APIResponse } from "@/lib/apiClient";

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  relevance_score?: number;
  skills_matched?: string[];
  skills_gaps?: string[];
}

export const jobService = {
  /**
   * Searches aggregated jobs from backend index based on query criteria.
   */
  search: async (params: {
    keyword?: string;
    location?: string;
    experience?: string;
    remote?: boolean;
  }): Promise<APIResponse<Job[]>> => {
    const query = new URLSearchParams();
    if (params.keyword) query.set("keyword", params.keyword);
    if (params.location) query.set("location", params.location);
    if (params.experience) query.set("experience", params.experience);
    if (params.remote !== undefined) query.set("remote", String(params.remote));

    return apiRequest<Job[]>(`/jobs/search?${query.toString()}`, {
      method: "GET",
    });
  },

  /**
   * Adds job to user's saved tracking dashboard index.
   */
  save: async (jobId: string): Promise<APIResponse<any>> => {
    return apiRequest<any>("/jobs/save", {
      method: "POST",
      bodyData: { job_id: jobId },
    });
  },

  /**
   * Retrieves user's saved/tracked job applications list.
   */
  getSaved: async (): Promise<APIResponse<Job[]>> => {
    return apiRequest<Job[]>("/jobs/saved", {
      method: "GET",
    });
  },
};

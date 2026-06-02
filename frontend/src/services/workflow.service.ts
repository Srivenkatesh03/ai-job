import { apiRequest, APIResponse } from "@/lib/apiClient";

export interface WorkflowRun {
  id: string;
  status: string;
  task_name: string;
  queue: string;
  created_at: string;
  logs?: string;
}

export const workflowService = {
  /**
   * Registers a new automation workflow chain.
   */
  create: async (workflowData: any): Promise<APIResponse<any>> => {
    return apiRequest<any>("/workflows", {
      method: "POST",
      bodyData: workflowData,
    });
  },

  /**
   * Dispatches task run trigger to designated Celery queue broker.
   */
  trigger: async (
    workflowId: string
  ): Promise<APIResponse<{ task_id: string; status: string }>> => {
    return apiRequest<{ task_id: string; status: string }>(`/workflows/${workflowId}/run`, {
      method: "POST",
    });
  },

  /**
   * Fetches active task/pipeline log statuses.
   */
  getStatus: async (workflowId: string): Promise<APIResponse<WorkflowRun>> => {
    return apiRequest<WorkflowRun>(`/workflows/${workflowId}/status`, {
      method: "GET",
    });
  },

  /**
   * Fetches all registered workflow runs belonging to the user.
   */
  getAll: async (): Promise<APIResponse<WorkflowRun[]>> => {
    return apiRequest<WorkflowRun[]>("/workflows", {
      method: "GET",
    });
  },
};

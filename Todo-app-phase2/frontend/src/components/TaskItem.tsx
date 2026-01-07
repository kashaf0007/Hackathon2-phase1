/**
 * TaskItem Component
 * Individual task display with completion toggle and delete
 */

"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { taskApi } from "src/lib/api";
import type { Task } from "../types/task";

interface TaskItemProps {
  task: Task;
  userId: string;
}

export function TaskItem({ task, userId }: TaskItemProps) {
  const queryClient = useQueryClient();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Toggle completion mutation
  const toggleMutation = useMutation({
    mutationFn: () =>
      taskApi.toggleComplete(userId, task.id, { completed: !task.completed }),
    onMutate: async () => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ["tasks"] });
      const previous = queryClient.getQueryData(["tasks"]);
      queryClient.setQueryData(["tasks"], (old: Task[] | undefined) =>
        old?.map((t) =>
          t.id === task.id ? { ...t, completed: !t.completed } : t
        )
      );
      return { previous };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(["tasks"], context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: () => taskApi.delete(userId, task.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setShowDeleteConfirm(false);
    },
  });

  return (
    <div className={`task-item ${task.completed ? 'task-completed' : ''}`}>
      <div className="task-item-content">
        {/* Completion checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => toggleMutation.mutate()}
          disabled={toggleMutation.isPending}
          className="task-checkbox"
        />

        {/* Task content */}
        <div className="task-details flex-1">
          <h3 className={`task-title ${task.completed ? 'completed' : ''}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`task-description ${task.completed ? 'completed' : ''}`}>
              {task.description}
            </p>
          )}
        </div>

        {/* Action buttons */}
        <div className="task-actions flex gap-sm">
          <button
            onClick={() => {
              if (typeof window !== "undefined") {
                window.location.href = `/tasks/${task.id}`;
              }
            }}
            className="btn btn-outline"
            disabled={toggleMutation.isPending}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            disabled={deleteMutation.isPending || toggleMutation.isPending}
            className="btn btn-outline text-danger-600 border-danger-300 hover:bg-danger-50 hover:border-danger-400"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </button>
        </div>
      </div>

      {/* Delete confirmation */}
      {showDeleteConfirm && (
        <div className="task-delete-confirmation card p-md mt-md">
          <p className="mb-md text-secondary-700">Are you sure you want to delete this task?</p>
          <div className="task-delete-actions flex gap-md">
            <button
              onClick={() => deleteMutation.mutate()}
              disabled={deleteMutation.isPending}
              className="btn btn-danger flex-1"
            >
              {deleteMutation.isPending ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Deleting...
                </>
              ) : "Yes, Delete"}
            </button>
            <button
              onClick={() => setShowDeleteConfirm(false)}
              disabled={deleteMutation.isPending}
              className="btn btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

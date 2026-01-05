/**
 * Task List Page
 * Main page for viewing and managing tasks
 */

"use client";

import { AuthGuard } from "@/components/AuthGuard";
import { TaskList } from "@/components/TaskList";

export default function TasksPage() {
  return (
    <AuthGuard>
      <div className="tasks-container">
        <header className="tasks-header">
          <h1>My Tasks</h1>
        </header>
        <TaskList />
      </div>
    </AuthGuard>
  );
}

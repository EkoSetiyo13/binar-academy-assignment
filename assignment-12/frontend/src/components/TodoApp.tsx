import React, { useState } from 'react';
import { ListsPanel, TasksPanel } from './panels';

export function TodoApp() {
  const [selectedListId, setSelectedListId] = useState<string | null>(null);

  const handleListSelect = (id: string) => {
    setSelectedListId(id);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Lists Panel */}
      <div className="lg:col-span-1">
        <ListsPanel
          selectedListId={selectedListId}
          onListSelect={handleListSelect}
        />
      </div>

      {/* Tasks Panel */}
      <div className="lg:col-span-2">
        <TasksPanel selectedListId={selectedListId} />
      </div>
    </div>
  );
} 
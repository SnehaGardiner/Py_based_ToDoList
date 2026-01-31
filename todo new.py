#!/usr/bin/env python3
"""
CLI To-Do List Application
A simple yet powerful command-line task management system

Features:
- Add tasks with priority levels
- View all tasks in a formatted table
- Mark tasks as complete
- Remove tasks
- Filter tasks by status
- Persistent storage (saves to file)
"""

import json
import os
from datetime import datetime
from typing import List, Dict

# File to store tasks persistently
TASKS_FILE = "tasks.json"

class TodoList:
    """Main class to manage the to-do list"""
    
    def __init__(self):
        """Initialize the to-do list and load existing tasks"""
        self.tasks: List[Dict] = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file if it exists"""
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, 'r') as file:
                    self.tasks = json.load(file)
                print(f"✓ Loaded {len(self.tasks)} tasks from storage")
            except json.JSONDecodeError:
                print("⚠ Warning: Could not read tasks file, starting fresh")
                self.tasks = []
        else:
            print("📝 Starting with a fresh to-do list")
    
    def save_tasks(self):
        """Save tasks to JSON file for persistence"""
        try:
            with open(TASKS_FILE, 'w') as file:
                json.dump(self.tasks, file, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")
            return False
    
    def add_task(self, description: str, priority: str = "medium"):
        """
        Add a new task to the list
        
        Args:
            description: The task description
            priority: Task priority (low, medium, high)
        """
        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority.lower() not in valid_priorities:
            priority = "medium"
        
        # Create task dictionary
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "priority": priority.lower(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_at": None
        }
        
        # Add to list and save
        self.tasks.append(task)
        self.save_tasks()
        
        print(f"\n✅ Task added successfully!")
        print(f"   ID: {task['id']}")
        print(f"   Description: {task['description']}")
        print(f"   Priority: {task['priority'].upper()}")
    
    def view_tasks(self, filter_status: str = "all"):
        """
        Display all tasks in a formatted table
        
        Args:
            filter_status: Filter by 'all', 'pending', or 'completed'
        """
        if not self.tasks:
            print("\n📭 Your to-do list is empty!")
            return
        
        # Filter tasks based on status
        filtered_tasks = self.tasks
        if filter_status == "pending":
            filtered_tasks = [t for t in self.tasks if not t["completed"]]
        elif filter_status == "completed":
            filtered_tasks = [t for t in self.tasks if t["completed"]]
        
        if not filtered_tasks:
            print(f"\n📭 No {filter_status} tasks found!")
            return
        
        # Print header
        print(f"\n{'='*80}")
        print(f"  YOUR TO-DO LIST - {filter_status.upper()} TASKS")
        print(f"{'='*80}")
        
        # Print column headers
        print(f"{'ID':<5} {'Status':<10} {'Priority':<10} {'Description':<35} {'Created':<15}")
        print(f"{'-'*80}")
        
        # Print each task
        for task in filtered_tasks:
            # Format status with emoji
            status = "✓ Done" if task["completed"] else "○ Pending"
            
            # Format priority with color indicators
            priority_map = {
                "high": "🔴 HIGH",
                "medium": "🟡 MEDIUM",
                "low": "🟢 LOW"
            }
            priority = priority_map.get(task["priority"], task["priority"])
            
            # Truncate long descriptions
            description = task["description"]
            if len(description) > 33:
                description = description[:30] + "..."
            
            # Format created date
            created = task["created_at"].split()[0]  # Just the date
            
            # Print task row
            print(f"{task['id']:<5} {status:<10} {priority:<10} {description:<35} {created:<15}")
        
        print(f"{'-'*80}")
        print(f"Total: {len(filtered_tasks)} tasks")
        print(f"{'='*80}\n")
    
    def complete_task(self, task_id: int):
        """
        Mark a task as completed
        
        Args:
            task_id: The ID of the task to complete
        """
        # Find task by ID
        task = self.find_task_by_id(task_id)
        
        if not task:
            print(f"\n❌ Task with ID {task_id} not found!")
            return
        
        if task["completed"]:
            print(f"\n⚠ Task {task_id} is already completed!")
            return
        
        # Mark as completed
        task["completed"] = True
        task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.save_tasks()
        
        print(f"\n🎉 Task completed!")
        print(f"   ID: {task['id']}")
        print(f"   Description: {task['description']}")
    
    def remove_task(self, task_id: int):
        """
        Remove a task from the list
        
        Args:
            task_id: The ID of the task to remove
        """
        # Find task by ID
        task = self.find_task_by_id(task_id)
        
        if not task:
            print(f"\n❌ Task with ID {task_id} not found!")
            return
        
        # Confirm deletion
        print(f"\n⚠ Are you sure you want to delete this task?")
        print(f"   ID: {task['id']}")
        print(f"   Description: {task['description']}")
        confirmation = input("   Type 'yes' to confirm: ").lower()
        
        if confirmation == 'yes':
            self.tasks.remove(task)
            # Reassign IDs to maintain order
            self.reassign_ids()
            self.save_tasks()
            print(f"\n🗑️  Task deleted successfully!")
        else:
            print(f"\n↩️  Deletion cancelled")
    
    def find_task_by_id(self, task_id: int) -> Dict:
        """
        Find a task by its ID
        
        Args:
            task_id: The ID to search for
            
        Returns:
            The task dictionary if found, None otherwise
        """
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def reassign_ids(self):
        """Reassign task IDs after deletion to maintain sequential order"""
        for index, task in enumerate(self.tasks, start=1):
            task["id"] = index
    
    def clear_completed(self):
        """Remove all completed tasks"""
        completed_count = len([t for t in self.tasks if t["completed"]])
        
        if completed_count == 0:
            print("\n📭 No completed tasks to clear!")
            return
        
        print(f"\n⚠ This will remove {completed_count} completed task(s).")
        confirmation = input("   Type 'yes' to confirm: ").lower()
        
        if confirmation == 'yes':
            self.tasks = [t for t in self.tasks if not t["completed"]]
            self.reassign_ids()
            self.save_tasks()
            print(f"\n🗑️  Cleared {completed_count} completed task(s)!")
        else:
            print(f"\n↩️  Operation cancelled")
    
    def get_statistics(self):
        """Display task statistics"""
        total = len(self.tasks)
        if total == 0:
            print("\n📊 No tasks to analyze!")
            return
        
        completed = len([t for t in self.tasks if t["completed"]])
        pending = total - completed
        
        high_priority = len([t for t in self.tasks if t["priority"] == "high" and not t["completed"]])
        medium_priority = len([t for t in self.tasks if t["priority"] == "medium" and not t["completed"]])
        low_priority = len([t for t in self.tasks if t["priority"] == "low" and not t["completed"]])
        
        completion_rate = (completed / total) * 100 if total > 0 else 0
        
        print(f"\n{'='*50}")
        print(f"  📊 TASK STATISTICS")
        print(f"{'='*50}")
        print(f"  Total Tasks:       {total}")
        print(f"  ✓ Completed:       {completed}")
        print(f"  ○ Pending:         {pending}")
        print(f"  Completion Rate:   {completion_rate:.1f}%")
        print(f"{'-'*50}")
        print(f"  Pending by Priority:")
        print(f"    🔴 High:         {high_priority}")
        print(f"    🟡 Medium:       {medium_priority}")
        print(f"    🟢 Low:          {low_priority}")
        print(f"{'='*50}\n")


def print_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("  📝 TO-DO LIST MANAGER")
    print("="*50)
    print("  1. ➕ Add a new task")
    print("  2. 📋 View all tasks")
    print("  3. 👁️  View pending tasks")
    print("  4. ✅ View completed tasks")
    print("  5. ✓  Mark task as complete")
    print("  6. ❌ Remove a task")
    print("  7. 🗑️  Clear completed tasks")
    print("  8. 📊 Show statistics")
    print("  9. 🚪 Exit")
    print("="*50)


def main():
    """Main function to run the to-do list application"""
    # Create TodoList instance
    todo_list = TodoList()
    
    # Welcome message
    print("\n" + "="*50)
    print("  🎯 WELCOME TO YOUR TO-DO LIST MANAGER!")
    print("="*50)
    
    # Main loop
    while True:
        print_menu()
        choice = input("\n👉 Enter your choice (1-9): ").strip()
        
        if choice == "1":
            # Add a new task
            print("\n➕ ADD NEW TASK")
            print("-" * 50)
            description = input("Task description: ").strip()
            
            if not description:
                print("❌ Task description cannot be empty!")
                continue
            
            print("\nPriority levels:")
            print("  1. Low")
            print("  2. Medium (default)")
            print("  3. High")
            priority_choice = input("Select priority (1-3, press Enter for Medium): ").strip()
            
            priority_map = {"1": "low", "2": "medium", "3": "high"}
            priority = priority_map.get(priority_choice, "medium")
            
            todo_list.add_task(description, priority)
        
        elif choice == "2":
            # View all tasks
            todo_list.view_tasks("all")
        
        elif choice == "3":
            # View pending tasks
            todo_list.view_tasks("pending")
        
        elif choice == "4":
            # View completed tasks
            todo_list.view_tasks("completed")
        
        elif choice == "5":
            # Mark task as complete
            print("\n✓ COMPLETE TASK")
            print("-" * 50)
            try:
                task_id = int(input("Enter task ID to mark as complete: "))
                todo_list.complete_task(task_id)
            except ValueError:
                print("❌ Invalid input! Please enter a valid task ID.")
        
        elif choice == "6":
            # Remove a task
            print("\n❌ REMOVE TASK")
            print("-" * 50)
            try:
                task_id = int(input("Enter task ID to remove: "))
                todo_list.remove_task(task_id)
            except ValueError:
                print("❌ Invalid input! Please enter a valid task ID.")
        
        elif choice == "7":
            # Clear completed tasks
            todo_list.clear_completed()
        
        elif choice == "8":
            # Show statistics
            todo_list.get_statistics()
        
        elif choice == "9":
            # Exit
            print("\n" + "="*50)
            print("  👋 Thank you for using To-Do List Manager!")
            print("  💾 All your tasks have been saved.")
            print("="*50 + "\n")
            break
        
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 9.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*50)
        print("  👋 Goodbye! Your tasks have been saved.")
        print("="*50 + "\n")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please restart the application.\n")
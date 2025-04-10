import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeView,
                              QPushButton, QInputDialog, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import QDir, Qt, pyqtSignal
from PyQt6.QtGui import QFileSystemModel

class FileExplorer(QWidget):
    file_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Button layout
        self.button_layout = QHBoxLayout()
        
        # New File button
        self.new_file_btn = QPushButton("New File")
        self.new_file_btn.clicked.connect(self.create_new_file)
        self.button_layout.addWidget(self.new_file_btn)
        
        # New Folder button
        self.new_folder_btn = QPushButton("New Folder")
        self.new_folder_btn.clicked.connect(self.create_new_folder)
        self.button_layout.addWidget(self.new_folder_btn)
        
        # Delete button
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_selected)
        self.button_layout.addWidget(self.delete_btn)
        
        self.layout.addLayout(self.button_layout)
        
        # Set up the file system model
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        
        # Set up the tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath()))
        
        # Hide unnecessary columns
        self.tree_view.setColumnWidth(0, 250)
        for i in range(1, 4):
            self.tree_view.hideColumn(i)
            
        # Connect double-click signal
        self.tree_view.doubleClicked.connect(self.item_double_clicked)
        
        self.layout.addWidget(self.tree_view)
        
    def item_double_clicked(self, index):
        """Handle double-click on a file"""
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.file_selected.emit(file_path)
    
    def create_new_file(self):
        """Create a new file in the selected directory"""
        current_index = self.tree_view.currentIndex()
        if not current_index.isValid():
            current_index = self.model.index(QDir.currentPath())
            
        # Get directory path
        path = self.model.filePath(current_index)
        if not os.path.isdir(path):
            path = os.path.dirname(path)
            
        # Get file name from user
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        
        if ok and file_name:
            file_path = os.path.join(path, file_name)
            try:
                with open(file_path, 'w') as f:
                    pass  # Create empty file
                # Select the new file
                new_index = self.model.index(file_path)
                self.tree_view.setCurrentIndex(new_index)
                self.file_selected.emit(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")
                
    def create_new_folder(self):
        """Create a new folder in the selected directory"""
        current_index = self.tree_view.currentIndex()
        if not current_index.isValid():
            current_index = self.model.index(QDir.currentPath())
            
        # Get directory path
        path = self.model.filePath(current_index)
        if not os.path.isdir(path):
            path = os.path.dirname(path)
            
        # Get folder name from user
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        
        if ok and folder_name:
            folder_path = os.path.join(path, folder_name)
            try:
                os.makedirs(folder_path, exist_ok=True)
                # Select the new folder
                new_index = self.model.index(folder_path)
                self.tree_view.setCurrentIndex(new_index)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {str(e)}")
                
    def delete_selected(self):
        """Delete the selected file or folder"""
        current_index = self.tree_view.currentIndex()
        if not current_index.isValid():
            return
            
        path = self.model.filePath(current_index)
        name = os.path.basename(path)
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}") 
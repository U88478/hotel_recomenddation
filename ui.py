import sys

from PyQt5 import QtWidgets, uic

from algorithms import insertion_sort, selection_sort, bubble_sort
from complete_data import load_data


class HotelApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(HotelApp, self).__init__()
        uic.loadUi('untitled.ui', self)

        # Debug: Confirm the UI is loaded
        print("UI Loaded")

        # Connect buttons to functions
        self.SortButton.clicked.connect(self.sort_hotels)
        self.DownloadButton.clicked.connect(self.download_results)
        print("Buttons connected")

        # Load hotel data
        self.file_path = 'hotel_info_dedup.csv'
        self.hotels = load_data(self.file_path)
        print(f"Loaded {len(self.hotels)} hotels")

        # Store algorithm's name etc
        self.sort_algorithm = ""
        self.sort_criterion = ""
        self.execution_time = ""

    def sort_hotels(self):
        try:
            # Get selected criteria from the boxes
            self.sort_algorithm = self.SortComboBox.currentText()
            property_to_sort = self.PropertiesComboBox.currentText()

            print(f"Sorting using {self.sort_algorithm} by {property_to_sort}")

            # Match properties
            property_map = {
                "Hotel Rating": "hotel_rating",
                "Hotel Experience": "hotel_experience",
                "Amenities": "amenity_count",
                "Price": "price"
            }

            key = property_map.get(property_to_sort, 'hotel_rating')
            self.sort_criterion = property_to_sort

            # 'amenity_count' is calculated if sorting by amenities
            if key == 'amenity_count':
                for hotel in self.hotels:
                    hotel['amenity_count'] = len(hotel['amenities'])

            # Sort based on the selected algorithm
            if self.sort_algorithm == "Insertion Sort":
                result = insertion_sort(self.hotels, key)
            elif self.sort_algorithm == "Selection Sort":
                result = selection_sort(self.hotels, key)
            elif self.sort_algorithm == "Bubble Sort":
                result = bubble_sort(self.hotels, key)

            # Display the results
            self.display_results(self.sort_algorithm, result, property_to_sort)
        except Exception as e:
            print(f"Error in sort_hotels: {e}")

    def display_results(self, sort_algorithm, result, criterion):
        try:
            self.results.clear()
            self.execution_time = f"{result['time']:.6f}"
            self.ExecutionLabel.setText(f"{sort_algorithm} Execution Time: {self.execution_time} seconds")

            html_content = f"""
                    <h2 style="color: #2E8B57;">{criterion}</h2>
                    <ul style="list-style-type: none; padding: 0;">
                    """

            for hotel in result['sorted_hotels']:
                name = hotel['hotel_name']
                value = hotel[criterion.lower().replace(' ', '_')]
                if criterion.lower() == "amenities":
                    value = ", ".join(sorted(hotel['amenities']))
                html_content += f"""
                            <li style="margin-bottom: 10px; font-size: 13px">
                                <span style="font-weight: bold; color: #4682B4;">{name}</span> - {value}
                            </li>
                            """

            html_content += "</ul>"

            self.results.setHtml(html_content)
            print("Results displayed")
        except Exception as e:
            print(f"Error in display_results: {e}")

    def download_results(self):
        try:
            results_text = self.results.toPlainText()
            results_lines = results_text.split('\n')
            if len(results_lines) > 1:
                results_text = '\n'.join(results_lines[1:])
            result = (f"{self.sort_algorithm} by {self.sort_criterion} in {self.execution_time}s\n\n{results_text}")
            if result:
                file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save results", "",
                                                                     "Text Files (*.txt);; All Files (*)")
                if file_name:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(result)
                    print(f"Results saved to {file_name}")
        except Exception as e:
            print(f"Error in download_results: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HotelApp()
    window.show()
    sys.exit(app.exec_())

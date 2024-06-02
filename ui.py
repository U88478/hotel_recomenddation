import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QCheckBox

from algorithms import insertion_sort, selection_sort, bubble_sort
from complete_data import load_data


class HotelApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(HotelApp, self).__init__()
        uic.loadUi('untitled.ui', self)

        # Connect buttons
        self.SortButton.clicked.connect(self.sort_hotels)
        self.PropertiesComboBox.currentTextChanged.connect(self.on_criterion_change)
        print("Buttons connected")

        # Load hotel data
        self.file_path = 'hotel_info_dedup.csv'
        self.hotels = load_data(self.file_path)
        print(f"Loaded {len(self.hotels)} hotels")

        # Initialize UI
        self.sort_algorithm = "Insertion Sort"
        self.sort_criterion = ""
        self.execution_time = ""

        # Load amenities from file
        self.amenities_checkboxes = {}
        self.load_amenities()

        # Hide scroll area initially
        self.scrollArea.setVisible(False)
        self.initial_width = self.width()
        self.amenities_width = 200

    def load_amenities(self):
        try:
            with open('amenities_list.txt', 'r') as file:
                amenities = [line.strip("[]") for line in file.readlines()]
                am = []
                for amenity in amenities:
                    am.extend([amm.strip("'") for amm in amenity.split(", ")])

                for amenity in am:
                    checkbox = QCheckBox(amenity)
                    self.amenitiesLayout.addWidget(checkbox)
                    self.amenities_checkboxes[amenity] = checkbox
            print("Loaded amenities and created checkboxes.")
        except Exception as e:
            print(f"Error loading amenities: {e}")

    def on_criterion_change(self):
        if self.PropertiesComboBox.currentText() == "Amenities":
            self.scrollArea.setVisible(True)
            self.resize(self.initial_width + self.amenities_width, self.height())  # Adjust width to fit amenities
        else:
            self.scrollArea.setVisible(False)
            self.resize(self.initial_width, self.height())  # Adjust width back to original

    def filter_hotels_by_amenities(self, hotels, selected_amenities):
        if not selected_amenities:
            return hotels
        return [hotel for hotel in hotels if all(amenity in hotel['amenities'] for amenity in selected_amenities)]

    def sort_hotels(self):
        try:
            # Get selected criteria
            property_to_sort = self.PropertiesComboBox.currentText()

            print(f"Sorting using {self.sort_algorithm} by {property_to_sort}")

            # Filter hotels if sorting by amenities
            if property_to_sort == "Amenities":
                selected_amenities = [amenity for amenity, checkbox in self.amenities_checkboxes.items() if
                                      checkbox.isChecked()]
                filtered_hotels = self.filter_hotels_by_amenities(self.hotels, selected_amenities)
                key = "hotel_name"  # Sort by hotel name after filtering
            else:
                filtered_hotels = self.hotels
                property_map = {
                    "Hotel Rating": "hotel_rating",
                    "Hotel Experience": "hotel_experience",
                    "Price": "price"
                }
                key = property_map.get(property_to_sort, 'hotel_rating')

            # Sort based on the selected algorithm
            if self.sort_algorithm == "Insertion Sort":
                result = insertion_sort(filtered_hotels, key)
            elif self.sort_algorithm == "Selection Sort":
                result = selection_sort(filtered_hotels, key)
            elif self.sort_algorithm == "Bubble Sort":
                result = bubble_sort(filtered_hotels, key)
            else:
                raise ValueError(f"Unsupported sort algorithm: {self.sort_algorithm}")

            # Display results
            self.display_results(self.sort_algorithm, result, property_to_sort)
        except Exception as e:
            print(f"Error in sort_hotels: {e}")

    def display_results(self, sort_algorithm, result, criterion):
        try:
            self.results.clear()
            self.execution_time = f"{result['time']:.6f}"
            self.ExecutionLabel.setText(f"{sort_algorithm} Execution Time: {self.execution_time} seconds")

            html_content = """
            <style>
                h2 {
                    color: #2E8B57;
                    text-align: center;
                    font-family: 'Arial', sans-serif;
                    border-bottom: 2px solid #2E8B57;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                }
                li {
                    margin-bottom: 10px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-family: 'Arial', sans-serif;
                }
                li:hover {
                    background-color: #f0f8ff;
                }
                li:nth-child(even) {
                    background-color: #f9f9f9;
                }
                li b {
                    font-weight: bold;
                    color: #4682B4;
                    font-size: 16px;
                }
                li span {
                    color: #555;
                    font-size: 14px;
                }
            </style>
            <h2>%s</h2>
            <ul>
            """ % criterion

            for hotel in result['sorted_hotels']:
                name = hotel['hotel_name']
                value = hotel[criterion.lower().replace(' ', '_')]
                if criterion.lower() == "amenities":
                    value = ", ".join(hotel['amenities'])
                html_content += f"""
                <li>
                    <b>{name}</b> - <span>{value}</span>
                </li>
                """

            html_content += "</ul>"

            self.results.setHtml(html_content)
            print("Results displayed")
        except Exception as e:
            print(f"Error in display_results: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HotelApp()
    window.show()
    sys.exit(app.exec_())

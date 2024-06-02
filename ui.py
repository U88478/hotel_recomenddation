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
        self.DownloadButton.clicked.connect(self.download_results)
        self.PropertiesComboBox.currentTextChanged.connect(self.on_criterion_change)
        self.OrderBox.currentTextChanged.connect(self.on_order_change)
        print("Buttons connected")

        # Load hotel data
        self.file_path = 'hotel_info_dedup.csv'
        self.hotels = load_data(self.file_path)
        print(f"Loaded {len(self.hotels)} hotels")

        # Initialize UI
        self.sort_algorithm = ""
        self.sort_criterion = ""
        self.selected_amenities = []
        self.order = -1
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

    def on_order_change(self):
        self.order = -1 if self.OrderBox.currentText() == "Descending" else 1

    def on_criterion_change(self):
        if self.PropertiesComboBox.currentText() == "Amenities":
            self.scrollArea.setVisible(True)
            self.resize(self.initial_width + self.amenities_width, self.height())  # Adjust width to fit amenities
        else:
            self.scrollArea.setVisible(False)
            self.resize(self.initial_width, self.height())  # Adjust width back to original

    def filter_hotels_by_amenities(self, hotels):
        if not self.selected_amenities:
            return hotels
        return [hotel for hotel in hotels if all(amenity in hotel['amenities'] for amenity in self.selected_amenities)]

    def sort_hotels(self):
        try:
            # Get selected criteria
            self.sort_algorithm = self.SortComboBox.currentText()
            self.sort_criterion = self.PropertiesComboBox.currentText()

            print(f"Sorting using {self.sort_algorithm} by {self.sort_criterion} {self.order}")

            # Filter hotels if sorting by amenities
            if self.sort_criterion == "Amenities":
                self.selected_amenities = [amenity for amenity, checkbox in self.amenities_checkboxes.items() if
                                           checkbox.isChecked()]
                filtered_hotels = self.filter_hotels_by_amenities(self.hotels)
                key = "hotel_name"  # Sort by hotel name after filtering
            else:
                filtered_hotels = self.hotels
                property_map = {
                    "Hotel Rating": "hotel_rating",
                    "Hotel Experience": "hotel_experience",
                    "Price": "price"
                }
                key = property_map.get(self.sort_criterion, 'hotel_rating')

            # Sort based on the selected algorithm
            match self.sort_algorithm:
                case "Insertion Sort":
                    result = insertion_sort(filtered_hotels, key, self.order)
                case "Selection Sort":
                    result = selection_sort(filtered_hotels, key, self.order)
                case "Bubble Sort":
                    result = bubble_sort(filtered_hotels, key, self.order)
                case _:
                    raise ValueError(f"Unsupported sort algorithm: {self.sort_algorithm}")

            self.execution_time = f"{result['time']:.6f}"
            print(f"Execution time: {self.execution_time}")

            # Display results
            self.display_results(self.sort_algorithm, result, self.sort_criterion)
        except Exception as e:
            print(f"Error in sort_hotels: {e}")

    def display_results(self, sort_algorithm, result, criterion):
        try:
            self.results.clear()
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
                .highlight {
                    font-weight: bold;
                    color: #FF4500;
                }
            </style>
            <h2>%s</h2>
            <ol>
            """ % criterion

            for hotel in result['sorted_hotels']:
                name = hotel['hotel_name']
                value = hotel[criterion.lower().replace(' ', '_')]
                if criterion.lower() == "amenities":
                    value = ", ".join(
                        [f"<span class='highlight'>{amenity}</span>" if amenity in self.selected_amenities
                         else amenity for amenity in hotel['amenities']]
                    )
                html_content += f"""
                <li>
                    <b>{name}</b> - <span>{value}</span>
                </li>
                """

            html_content += "</ol>"

            self.results.setHtml(html_content)
            print("Results displayed")
        except Exception as e:
            print(f"Error in display_results: {e}")

    def download_results(self):
        try:
            results = ((
                           f"{self.sort_algorithm} by {self.sort_criterion}{self.selected_amenities if self.selected_amenities else ""}"
                           f" in {"Ascending" if self.order == 1 else "Descending"} order in {self.execution_time}s\n\n")
                       + "\n".join([result for result in self.results.toPlainText().split("\n")[1:]]))
            if results:
                file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save results", "",
                                                                     "Text Files (*.txt);;All Files (*)")
                if file_name:
                    with open(file_name, 'w') as file:
                        file.write("".join([result for result in results]))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HotelApp()
    window.show()
    sys.exit(app.exec_())

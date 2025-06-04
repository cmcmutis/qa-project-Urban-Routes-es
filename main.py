from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import data
from methodshomepage import UrbanRoutesPage, retrieve_phone_code
from selenium.webdriver.chrome.service import Service


# PRUEBAS
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.add_argument("--enable-logging")
        cls.driver = webdriver.Chrome(service=Service("/opt/homebrew/bin/chromedriver"), options=options)
        cls.methods = UrbanRoutesPage(cls.driver)

# PRUEBA 1 CONFIGURAR LA DIRECCION
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

 # PRUEBA 2 SELECCIONAR LA TARIFA COMFORT
    def test_select_comfort_rate_icon(self):
            self.test_set_route()
            routes_pages = UrbanRoutesPage(self.driver)
            routes_pages.click_on_order_taxi_button()
            routes_pages.click_on_comfort_rate_icon()
            comfort_rate = routes_pages.get_comfort_rate_icon().text
            comfort_text = "Comfort"

            assert comfort_rate in comfort_text


# PRUEBA 3 RELLENAR EL NUMERO TELEFONICO
    def test_set_phone_number(self):
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_on_phone_number_field_one()
        routes_pages.set_phone_number_field_two()
        routes_pages.click_next_button()
        routes_pages.set_code_number()
        routes_pages.click_confirm_button()

        assert routes_pages.get_phone_number_value() == '+1 123 123 12 12'

# PRUEBA 4 AGREGAR TARJETA DE CREDITO
    def test_set_card_number(self):
        self.test_set_phone_number()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_card_number_field()
        routes_pages.get_add_new_card_number_button()
        routes_pages.set_new_card_number()
        routes_pages.get_cvv_field()
        routes_pages.set_cvv_number()
        routes_pages.get_confirm_add_card_button()

        assert routes_pages.new_card_value() == '1234 5678 9100'
        assert routes_pages.get_cvv_value() == '111'

# PRUEBA 5 ESCRIBIR UN MENSAJE PARA EL CONTROLADOR.
    def test_send_message_for_driver(self):
        self.test_select_comfort_rate_icon()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_comment_field()
        routes_pages.set_message_for_driver()

        assert routes_pages.message_for_driver() == 'Traiga un aperitivo'

# PRUEBA 6 PEDIR UNA MANTA Y PAÑUELOS
    def test_order_blanket(self):
        self.test_send_message_for_driver()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_blanket_button()
        assert routes_pages.switch_button_active().is_selected() == True


# PRUEBA 7 PEDIR 2 HELADOS
    def test_order_two_ice_cream(self):
        self.test_order_blanket()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_ice_cream_button_plus()
        routes_pages.click_ice_cream_button_plus()
        routes_pages.click_ice_cream_button_plus()
        routes_pages.ice_cream_counter_value()

        assert routes_pages.ice_cream_counter_value() == '2'

# PRUEBA 8 APARECE EL MODAL PARA BUSCAR UN TAXI
    def test_find_a_car(self):
        self.test_order_two_ice_cream()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_find_a_car()
        assert routes_pages.serch_a_car_screen() == 'Buscar automóvil'

# PRUEBA 9 ESPERAR A QUE APAREZCA LA INFORMACION DEL CONDUCTOR EN EL MODAL
    def test_driver_information(self):
        self.test_find_a_car()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_timeout_modal()
        assert routes_pages.order_shown().is_displayed() == True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

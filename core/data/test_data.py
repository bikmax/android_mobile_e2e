from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


class TestData:

    FEEDBACK_BTN = (By.XPATH, '//android.widget.Button[@content-desc="Написать"]')
    CUSTOM_WISH_PRICE_ALERT = (By.XPATH, '//android.view.View[@content-desc="Стоимость должна быть больше 0"]')
    CLEAR_TF = (By.XPATH, '//android.view.View[@resource-id="custom_wish_link_field"]/android.widget.ImageView')
    WRONG_LINK_ALERT = (By.XPATH, '//android.view.View[@content-desc="Неправильная ссылка"]')
    AI_RESULT_1 = (By.XPATH, '(//android.view.View[contains(@content-desc, "₽")])[1]')
    friend_have_no_wishes = (By.XPATH, '//android.view.View[@content-desc="Нет желаний"]')
    BS_AUTH_TO_PROCEED = (By.XPATH, '//android.widget.Button[@content-desc="Авторизоваться"]')
    SKIP_BUTTON = (By.XPATH, '//android.widget.Button[@content-desc="Пропустить"]')
    UPDATED_PROFILE_BIRTH_DAY = (By.XPATH, '//android.view.View[@content-desc="12 декабря 24 года"]')
    UPDATED_PROFILE_NAME = (By.XPATH, '//android.view.View[@content-desc="Pervaya Egorova"]')
    DBAY_WIDGET = (By.XPATH, '//android.view.View[@content-desc="День рождения"]')
    CONTACT_GROUP_PPL_COUNT = (By.XPATH, '//android.view.View[@content-desc="1 контакт"]')
    NAME_CANNOT_BE_EMPTY = (By.XPATH, '//android.view.View[@content-desc="Поле не может быть пустым"]')
    FIELD_CANNOT_BE_EMPTY_1 = (By.XPATH, '(//android.view.View[@content-desc="Поле не может быть пустым"])[1]')
    FIELD_CANNOT_BE_EMPTY_2 = (By.XPATH, '(//android.view.View[@content-desc="Поле не может быть пустым"])[2]')



    USER_PROFILE_PHONENUMBER = (By.XPATH, '//android.view.View[@content-desc="81111111111115"]')
    AUTH_BYPHONE = (
        By.XPATH, '//android.widget.Button[@content-desc="По номеру телефона"]'
    )
    COME_IN =  (
        By.XPATH, '//android.view.View[contains(@content-desc, "ВОЙДИТЕ")]'
    )

    save_card_button = (By.XPATH, "//*[contains(text(), 'Сохранить карту')]")
    PROFILE_SETTINGS_USERNUMBER_MERGE = (By.XPATH, "//android.view.View[@content-desc='81111111111115']")
    PROFILE_SETTINGS_USERNUMBER = (By.XPATH, "//android.view.View[@content-desc='79640090555']")
    BRO_WAIT = (By.XPATH, '//android.view.View[contains(@content-desc, "Нужно немного подождать,")]')
    NO_FRIENDS = (By.XPATH, '//android.view.View[@content-desc="У вас пока нет друзей"]')
    CONFIRM_CODE = (By.XPATH, '//android.view.View[@content-desc="Введите код"]')
    ADD_BUTTON = "Screen_MyWishes_Button_CreateWishlist"
    PRIVACY_SOME_SELECT_FRIEND_1 = (By.XPATH, "//android.view.View[contains(@content-desc, '85555555555')]/android.widget.CheckBox")
    user1_name = "Test User1"

    friend1_name = "Firsty_NEW"
    friend2_name = "Vtoroy_NEW"
    friend3_name = "Treti_NEW"

    phone_friend1 = "1111111555"
    phone_friend2 = "2222222555"
    phone_friend3 = "3333333555"
    phone_friend4 = "4444444555"
    phone_friend5 = "5555555555"
    phone_friend6 = "6666666555"
    phone_friend7 = "7777777555"
    phone_friend8 = "8888888555"
    phone_friend9 = "9999999555"

    phone_prod_friend1 = "1111111555"
    phone_prod_friend2 = "2222222555"
    phone_prod_friend3 = "3333333555"
    phone_prod_friend4 = "4444444555"
    phone_prod_friend5 = "5555555555"
    phone_prod_friend6 = "6666666555"
    phone_prod_friend7 = "7777777555"
    phone_prod_friend8 = "8888888555"
    phone_prod_friend9 = "9999999555"

    phone_friend_alive = "56565656555"
    phone_friend_no_delete = "4321432498855"

    # ID
    AUTH_PHONE_FIELD = (By.XPATH, '//android.widget.EditText[@resource-id="auth_phone_field"]')
    AUTH_PHONE_FIELD_XP = (By.XPATH, '//android.widget.EditText[@resource-id="auth_phone_field"]')

    AUTH_CBX_TERMS = (By.XPATH, '//android.widget.CheckBox[@resource-id="Screen_RegistrationAgreement_Checkbox_AcceptTerms"]')
    AUTH_CBX_EMAIL = (By.XPATH, '//android.view.View[contains(@content-desc, "Я соглашаюсь на рассылку")]')
    BOTTOM_HOME_BTN = "bottom_home_btn"
    BOTTOM_HOME_BTN_XP = (By.XPATH, '//android.widget.ImageView[@content-desc="Вкладка 1 из 5"]')
    BOTTOM_CATALOG_BTN = (By.XPATH, '//android.widget.ImageView[@content-desc="Вкладка 2 из 5"]')
    BOTTOM_AI_BTN = "bottom_ai_btn"

    BOTTOM_FRIENDS_BTN_XP = (By.XPATH, '//android.widget.ImageView[@content-desc="Вкладка 4 из 5"]')

    BOTTOM_WISHES_BTN = (By.XPATH, '//android.widget.ImageView[@content-desc="Вкладка 5 из 5"]')

    BOTTOM_AI_BTN_XP = (By.XPATH, '//android.widget.ImageView[@content-desc="Вкладка 3 из 5"]')

    WISHES_100_FULL = (
        By.XPATH,
        '//android.view.View[contains(@content-desc, "Накоплено 100%")]'
    )

    WISH_IS_COMPLETING = (
        By.XPATH,
        '//android.view.View[contains(@content-desc, "Исполняется")]'
    )

    BOTTOM_CONFIRM_ACTION_BTN = (By.XPATH, '//android.widget.Button[@content-desc="Удалить"]')
    MAIN_PAGE_NOTIFICATIONS_BELL = (By.XPATH, '//android.view.View[@resource-id="main_page_notifications_bell"]')
    MAIN_PAGE_MY_WISHES_LIST_BUTTON = "main_page_my_wishes_list_button"
    MAIN_PAGE_WISHES_WITH_MY_PARTICIPATION_BUTTON = "main_page_wishes_with_my_participation_button"

    CUSTOM_WISH_LINK_FIELD = "custom_wish_link_field"
    CUSTOM_WISH_NAME_FIELD = "custom_wish_name_field"
    CUSTOM_WISH_PRICE_FIELD = "custom_wish_price_field"
    CUSTOM_WISH_DESC_FIELD = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_desc_field"]')

    CUSTOM_WISH_PHOTO_BTN_1 = "custom_wish_photo_btn_1"
    CUSTOM_WISH_PHOTO_BTN_2 = "custom_wish_photo_btn_2"
    CUSTOM_WISH_PHOTO_BTN_N = "custom_wish_photo_btn_N"

    PRIVACY_BUTTON_ALL = "ALL"
    PRIVACY_BUTTON_ONLYME = "NONE"
    PRIVACY_BUTTON_SOME = "FOR_CONTACTS"

    CUSTOM_WISH_WHERE_TO_FIND_FIELD = "custom_wish_wheretofind_field"

    CONTACTS_FRIEND_1 = "contacts_friend_0"
    CONTACTS_FRIEND_2 = "contacts_friend_1"
    CONTACTS_FRIEND_3 = "contacts_friend_2"
    CONTACTS_GROUPS = "contacts_my_groups"
    CONTACTS_OPENED_FRIEND_ADD_TO_FAVORITE = "Добавить в избранные"
    CONTACTS_OPENED_FRIEND_ADD_TO_FAVORITE2 = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Добавить в избранных"]'
    )
    CONTACTS_OPENED_FRIEND_SETTINGS = (
        By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView[3]'
    )

    CONTACTS_OPENED_FRIEND_SETTINGS_NOTIF_OFF = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Выключить уведомления"]'
    )

    CONTACTS_OPENED_FRIEND_SETTINGS_NOTIF_ON = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Включить уведомления"]'
    )

    CONTACTS_OPENED_FRIEND_SETTINGS_FEED_OFF = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Скрывать из ленты"]'
    )

    CONTACTS_OPENED_FRIEND_SETTINGS_FEED_ON = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Показывать в ленте"]'
    )

    CREATE_GROUP_TEXTFIELD = "create_group_textfield"
    CREATE_GROUP_FRIEND_SEARCH_FIELD = "create_group_friend_search_field"
    CREATE_GROUP_ADD_FRIEND_0 = "create_group_add_friend_0"
    CREATE_GROUP_ADD_FRIEND_1 = "create_group_add_friend_1"
    CREATE_GROUP_ADD_FRIEND_2 = "create_group_add_friend_2"
    CREATE_GROUP_ADD_FRIEND_N = "create_group_add_friend_N"
    CREATE_GROUP_SELECT_COVER_PICTURE_1 = "create_group_select_cover_picture_1"
    CREATE_GROUP_SELECT_COVER_PICTURE_2 = "create_group_select_cover_picture_2"
    CREATE_GROUP_SELECT_COVER_PICTURE_N = "create_group_select_cover_picture_N"
    MY_GROUPS_CREATE_GROUP_BUTTON = "my_groups_create_group_button"
    MY_GROUPS_OPEN_GROUP_1 = "my_groups_open_group_1"
    MY_GROUPS_OPEN_GROUP_2 = "my_groups_open_group_2"
    MY_GROUPS_OPEN_GROUP_N = "my_groups_open_group_N"
    MY_GROUPS_OPENED_GROUP_EDIT_BUTTON = "my_groups_opened_group_edit_button"
    MY_GROUPS_OPENED_GROUP_ADD_BUTTON = "my_groups_opened_group_add_button"
    MY_GROUPS_OPENED_GROUP_REMOVE_FRIEND_1 = "my_groups_opened_group_remove_friend_1"
    MY_GROUPS_OPENED_GROUP_REMOVE_FRIEND_2 = "my_groups_opened_group_remove_friend_2"
    MY_GROUPS_OPENED_GROUP_REMOVE_FRIEND_N = "my_groups_opened_group_remove_friend_N"
    MY_GROUPS_EDIT_GROUP_NAME_FIELD = "my_groups_edit_group_name_field"
    MY_GROUPS_EDIT_GROUP_DELETE_GROUP_BUTTON = "my_groups_edit_group_delete_group_button"

    FRIEND_WISH_1 = "friend_wish_0"
    FRIEND_WISH_KNIFES = (By.XPATH, '//android.view.View[contains(@content-desc, "ножей")]')


    FRIEND_WISH_2 = "friend_wish_2"
    FRIEND_WISH_N = "friend_wish_N"

    CATALOG_CATEGORIES_BTN = (By.XPATH, '//android.widget.ImageView[@content-desc="Категории"]')
    CATEGORY_LIST_ITEM_1 = "category_list_item_0"
    CATEGORY_LIST_ITEM_2 = "category_list_item_1"
    CATEGORY_LIST_ITEM_3 = "category_list_item_2"
    CATEGORY_LIST_ITEM_4 = "category_list_item_3"

    SUGGEST_WISH_FRIEND_1 = "suggest_wish_friend_1"
    SUGGEST_WISH_FRIEND_2 = "suggest_wish_friend_2"
    SUGGEST_WISH_FRIEND_N = "suggest_wish_friend_N"

    CATEGORY_ITEM_1 = "category_item_0"
    CATEGORY_ITEM_2 = "category_item_1"
    CATEGORY_ITEM_3 = "category_item_2"
    CATEGORY_ITEM_4 = "category_item_3"

    PAYMENT_CHOOSE_DONATE_OPTION = "payment_choose_donate_option"
    PAYMENT_CHOOSE_FULL_PAYMENT_OPTION = "payment_choose_full_payment_option"
    PAYMENT_DONATE_MONEY_AMOUNT_FIELD = "payment_donate_money_amount_field"
    PAYMENT_DONATE_SET_FULL_AMOUNT_BTN = "payment_donate_set_full_amount_btn"

    DELIVERY_OPTION_TO_PICKUP_POINT = "delivery_option_to_pickup_point"
    DELIVERY_OPTION_COURIER_TO_ADDRESS = "delivery_option_courier_to_adress"
    DELIVERY_CHOOSE_RECIPIENT = "delivery_choose_recipient"
    DELIVERY_CHOOSE_PICKUP_POINT = "delivery_choose_pickup_point"
    DELIVERY_CHOOSE_ADDRESS = "delivery_choose_address"

    RECIPIENT_NAME = "recipient_name"
    RECIPIENT_CHOOSE_USER = "recipient_choose_user"
    RECIPIENT_SECOND_NAME = "recipient_second_name"
    RECIPIENT_EMAIL = "recipient_email"
    RECIPIENT_PHONE = "recipient_phone"

    DELIVERY_PICKUP_POINT_SEARCH_FIELD = "delivery_pickup_point_search_field"
    DELIVERY_PICKUP_POINT_SEARCH_RESULT_1 = "delivery_pickup_point_search_result_0"
    DELIVERY_PICKUP_POINT_SEARCH_RESULT_2 = "delivery_pickup_point_search_result_1"
    DELIVERY_PICKUP_POINT_SEARCH_RESULT_3 = "delivery_pickup_point_search_result_3"
    DELIVERY_FOUND_PICKUP_POINT_ON_MAP = "delivery_found_pickup_point_on_map"


    COURIER_CITY_STREET_HOUSE = "courier_city_street_house"
    COURIER_KVARTIRA = "courier_kvartira"
    COURIER_PODEZD = "courier_podezd"
    COURIER_FLOOR = "courier_floor"
    COURIER_DOMOFON = "courier_domofon"
    COURIER_COMMENT = "courier_comment"

    AI_BEGIN_FOR_SELF = "AI_begin_for_self"
    AI_BEGIN_FOR_FRIEND = "AI_begin_for_friend"
    AI_SEARCH_FIELD = (By.XPATH, '//android.widget.EditText[@resource-id="AI_SEARCH_FIELD"]')
    AI_SEND_MESSAGE = "AI_SEND_MESSAGE"
    AI_START_SEARCH = "AI_START_SEARCH"

    TRANSFER_MONEY_BETWEEN_WISH_FROM = "transfer_money_between_wish_FROM"
    TRANSFER_MONEY_BETWEEN_WISH_TO = "transfer_money_between_wish_TO"
    TRANSFER_MONEY_BETWEEN_WISH_CHOOSE_FROM_1 = "transfer_money_between_wish_choose_FROM_1"
    TRANSFER_MONEY_BETWEEN_WISH_CHOOSE_FROM_2 = "transfer_money_between_wish_choose_FROM_2"
    TRANSFER_MONEY_BETWEEN_WISH_CHOOSE_FROM_N = "transfer_money_between_wish_choose_FROM_N"
    TRANSFER_MONEY_BETWEEN_WISH_CHOOSE_TO_1 = "transfer_money_between_wish_choose_TO_1"
    TRANSFER_MONEY_BETWEEN_WISH_CHOOSE_TO_2 = "transfer_money_between_wish_choose_TO_2"
    TRANSFER_MONEY_BETWEEN_WISH_CHOOSE_TO_N = "transfer_money_between_wish_choose_TO_N"
    TRANSFER_BETWEEN_WISH_MONEY_AMOUNT_FIELD = "transfer_between_wish_money_amount_field"

    PERSONAL_PROFILE_LOGOUT_BUTTON = "personal_profile_logout_button"
    PERSONAL_PROFILE_BALANCE_AND_TRANSFERS = "personal_profile_balance_and_transfers"
    PERSONAL_PROFILE_ACTIVE_WISHES = "personal_profile_active_wishes"
    PERSONAL_PROFILE_RECEIVED_WISHES = "personal_profile_recieved_wishes"
    PERSONAL_PROFILE_CONTRIBUTED_WISHES = "personal_profile_contributed_wishes"
    PERSONAL_PROFILE_PERSONAL_DATA = "personal_profile_personal_data"
    PERSONAL_PROFILE_EMAIL_AND_SECURITY = "personal_profile_email_and_security"

    PERSONAL_PROFILE_AVATAR = "personal_profile_avatar"
    PERSONAL_DATA_NAME = "personal_data_name"
    PERSONAL_DATA_SECOND_NAME = "personal_data_second_name"
    PERSONAL_DATA_CHOOSE_GENDER = "personal_data_choose_gender"
    PERSONAL_DATA_CHOOSE_GENDER_M = "personal_data_choose_gender_M"
    PERSONAL_DATA_CHOOSE_GENDER_F = "personal_data_choose_gender_F"
    PERSONAL_DATA_BIRTH_DAY_DATE = "personal_data_birth_day_date"

    PERSONAL_EMAIL_EDIT_FIELD = "personal_email_edit_field"

    REGISTER_NEW_USER_CBX_TERMS = "register_new_user_cbx_terms"
    REGISTER_NEW_USER_CBX_EMAIL = "register_new_user_cbx_email"
    REGISTER_NEW_USER_NAME = "register_new_user_name"
    REGISTER_NEW_USER_SECOND_NAME = "register_new_user_second_name"
    REGISTER_NEW_USER_BIRTHDAY_DATE = "register_new_user_birthday_date"
    REGISTER_NEW_USER_GENDER = "register_new_user_gender"
    REGISTER_NEW_USER_GENDER_M = "register_new_user_gender_M"
    REGISTER_NEW_USER_GENDER_F = "register_new_user_gender_F"
    REGISTER_NEW_USER_EMAIL = "register_new_user_email"

    MY_WISHES_WISHLIST_CREATE = "Screen_MyWishes_Button_CreateWishlist"
    MY_WISHES_WISHLIST_CREATE_NAME_FIELD = "Screen_CreateWishList_FormField_Name"
    MY_WISHES_WISHLIST_EVENTDATE_FIELD = "Screen_CreateWishList_Form_NewList_Field_EventDate"
    MY_WISHES_WISHLIST_SEARCH_WISHES_TO_ADD = "my_wishes_wishlist_search_wishes_to_add"
    MY_WISHES_WISHLIST_ADD_WISH_1 = "Screen_CreateWishList_Form_Wishes_ListView_Products_Item_0"
    MY_WISHES_WISHLIST_ADD_WISH_2 = "Screen_CreateWishList_Form_Wishes_ListView_Products_Item_1"
    MY_WISHES_WISHLIST_ADD_WISH_3 = "Screen_CreateWishList_Form_Wishes_ListView_Products_Item_2"
    MY_WISHES_ALL_SHOW_TAB = "my_wishes_all_show_tab"
    MY_WISHES_WISHLIST_SHOW_TAB = "my_wishes_wishlist_show_tab"
    MY_WISHES_WISHLIST_CHOOSE_1 = "Screen_MyWishes_ListView_Item_0"
    MY_WISHES_WISHLIST_CHOOSE_2 = "my_wishes_wishlist_choose_2"
    MY_WISHES_WISHLIST_CHOOSE_N = "my_wishes_wishlist_choose_N"
    MY_WISHES_WISHLIST_EDIT_BUTTON = "Screen_WishList_AppBar_Button_Edit"
    MY_WISHES_WISHLIST_EDIT_NAME_FIELD = "Screen_EditWishList_Form_List_Field_Name"
    MY_WISHES_WISHLIST_EDIT_EVENTDATE_FIELD = "Screen_EditWishList_Form_List_Field_EventDate"
    MY_WISHES_WISHLIST_EDIT_ADD_WISH = "Screen_EditWishList_Button_AddWish"
    MY_WISHES_WISHLIST_EDIT_REMOVE_WISH_1 = (By.XPATH, '//android.view.View[@resource-id="Screen_EditWishList_ListView_Wishes_Button_Delete_Item_0"]/android.widget.ImageView')
    MY_WISHES_WISHLIST_EDIT_REMOVE_WISH_2 = "my_wishes_wishlist_edit_remove_wish_2"
    MY_WISHES_WISHLIST_EDIT_DELETE_WISHLIST = (By.XPATH, '//android.widget.ImageView[@content-desc="Удалить список желаний"]')





    #bounds
    #auth
    auth_phone_number_field = "[53,572][1028,731]"
    auth_resend_code = (By.XPATH, '//android.widget.ImageView[@content-desc="Получить код повторно"]')


    #notif
    notification_bell = "main_page_notifications_bell_has_notifications"
    notifications_see_top_wish = "[368,675][659,801]"
    notification_bell_have = "main_page_notifications_bell_has_notifications"
    notification_bell_have_1 = (By.XPATH, '//android.widget.ImageView[@content-desc="1"]')
    notification_bell_have_2 = (By.XPATH, '//android.widget.ImageView[@content-desc="2"]')
    notification_bell_with_not = (By.XPATH, '//android.view.View[@resource-id="main_page_notifications_bell_has_notifications"]')




    first_friend_bonds = "[53,457][1028,756]"
    second_friend_bonds = "[53,756][1028,1055]"
    third_friend_bonds = "[53,1110][1028,1328]"
    #register
    cbx_accept_terms1 = "[53,719][105,772]"
    cbx_accept_terms2 = "[53,1066][105,1118]"

    register_name = (By.XPATH, '//android.widget.EditText[@resource-id="Screen_RegistrationUserInfo_Form_Field_Name"]')
    register_second_name = (By.XPATH, '//android.widget.EditText[@resource-id="Screen_RegistrationUserInfo_Form_Field_Surname"]')


    register_bday = "Screen_RegistrationUserInfo_Form_Field_DateOfBirth"
    register_email = (By.XPATH, '//android.widget.EditText[@resource-id="Screen_RegistrationUserInfo_Form_Field_Email"]')
    register_email_id = "Screen_RegistrationUserInfo_Form_Field_Email"
    logout_button = (By.XPATH, '//android.view.View[@resource-id="personal_profile_logout_button"]')
    logout_confirm_button = (By.XPATH, '//android.widget.Button[@content-desc="Выйти"]')

    exit_confirm_button = (By.XPATH, '//android.widget.Button[@content-desc="Закрыть"]')
    avatar_bonds = "personal_profile_avatar"
    downloads_bonds = (By.XPATH, '//android.widget.TextView[@resource-id="com.google.android.apps.photos:id/title" and @text="Download"]')
    update_avatar_bonds = "[201,1490][504,1616]"
    pictue_first_pic_from_gallery = (By.XPATH, '//android.widget.ImageView[starts-with(@content-desc, "Photo taken on")]')
    picture_for_update_avatar_bonds = "[0,873][264,1137]"
    personal_data_bonds = (By.XPATH, '//android.widget.ImageView[@content-desc="Профиль\nличные данные"]')
    security_and_email_bonds = "[551,1239][1028,1716]"
    email_textfield_bonds = "[53,627][1028,786]"
    profile_help_button_bonds = (By.XPATH, '//android.widget.ImageView[@content-desc="Помощь"]')
    profile_help_email_tf = (By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[1]')
    profile_help_tema_tf = (By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[2]')
    profile_help_message_tf = (By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[3]')



    profile_name_bonds = "[53,627][1028,781]"
    profile_second_name_bonds = "[53,834][1028,992]"
    profile_gender_bonds = "[53,1045][1028,1199]"
    profile_gender_male_bonds = "[74,1222][1006,1367]"
    profile_gender_female_bonds = (By.XPATH, '//android.view.View[@content-desc="Женский"]')
    profile_date_of_birth_field_bonds = "[53,1251][1028,1405]"
    profile_date_of_birth_picker_bonds = "[943,1307][985,1349]"
    profile_delete_profile_bonds = (By.XPATH, '//android.widget.ImageView[@content-desc="Удалить профиль и все данные"]')
    profile_delete_confirm_bonds = (By.XPATH, '//android.widget.Button[@content-desc="Удалить"]')
    custom_wish_add_button = (By.XPATH, '//android.view.View[@content-desc="Добавить\nсвоё новое желание"]')
    decline_wish_final_button = "[337,2117][743,2277]"
    next_button = (By.XPATH, '//android.widget.Button[@content-desc="Далее"]')
    choose_friends_first = "85555555555"
    choose_friends_second = "[53,1152][1028,1370]"

    contacts_my_groups_button = (By.XPATH, '//android.widget.ImageView[@content-desc="Мои группы"]')
    create_group_button = (By.XPATH, '//android.widget.Button[@content-desc="Создать группу"]')
    create_group_text_field = (By.XPATH, '//android.widget.EditText[@resource-id="create_group_textfield"]')
    create_group_add_first_friend = "create_group_add_friend_0"
    create_group_choose_pic = "[551,903][789,1097]"
    my_groups_first_group = "my_groups_open_group_0"
    opened_group_edit_button = "my_groups_opened_group_edit_button"
    edit_group_name_field = "[53,627][1028,781]"
    opened_group_remove_member_button = "[964,1061][1028,1124]"
    opened_group_remove_member_confirm_button = "[331,1456][749,1616]"
    edit_group_delete_group = (By.XPATH, '//android.widget.ImageView[@content-desc="Удалить группу"]')
    edit_group_delete_group_confirm = (By.XPATH, '//android.widget.Button[@content-desc="Удалить"]')

    goods_list_first_good = "[53,446][530,1178]"

    #wishes
    MY_WISHES_FIRST_WISH = "Screen_MyWishes_Item_0"
    MY_WISHES_SECOND_WISH = "Screen_MyWishes_Item_1"
    MY_WISHES_OPENED_WISH_EDIT_BUTTON = (By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView[3]')
    MY_WISHES_EDIT_DELETE_BUTTON = (By.XPATH, '//android.widget.ImageView[@content-desc="Удалить желание"]')
    my_wish_second_wish = "[0,795][1080,1184]"
    receive_wish = (By.XPATH, '//android.widget.Button[@content-desc="Получить желание"]')
    wish_from_catalog_description_field = (By.XPATH, '//android.widget.EditText')
    added_wish_details_of_description_button = "[787,1204][1028,1254]"
    accept_suggested_wish_desc_field = "[53,1019][1028,1390]"
    suggested_partner_wish_privacy_only_me = "[53,905][1028,1039]"
    suggested_partner_wish_privacy_some = "[53,1288][1028,1422]"
    opened_wish_edit_button = "[954,74][1080,200]"
    wishes_show_all_whishes = (By.XPATH, '//android.widget.ImageView[@content-desc="Все"]')
    wishes_all_wishes_first_wish = (By.XPATH, '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View[2]/android.view.View')
    delete_wish_button = "[53,2064][524,2190]"

    transfer_money_from_wish = "[53,588][1028,806]"
    transfer_money_from_select_wish = "[84,536][996,801]"
    transfer_money_to_wish = "[53,1250][1028,1467]"
    transfer_money_to_select_wish = "[84,536][996,693]"
    transfer_money_amount_field = "[53,1551][1028,1656]"

    #catalog
    catalog_search_field = (By.XPATH, '//android.view.View[@content-desc="Поиск"]')
    partner_wish = "Renome"
    catalog_search_field_result = (By.XPATH, '//android.widget.ImageView[@content-desc="Renome"]')
    partner_wish_add_button = (By.XPATH, '//android.view.View[contains(@content-desc, "моих желаний")]')
    partner_wish_add_with_settings_button = "[928,1623][996,1671]"
    catalog_first_good = "[53,446][530,1178]"
    catalog_second_good = "[551,446][1028,1178]"
    catalog_third_good = "[53, 1262][530, 1994]"
    catalog_fourth_good = "[551,1262][1028,1994]"
    catalog_suggest_wish_first_friend = "[53,675][1028,893]"


    #payment
    payment_money_amount_field = "[53,1231][1028,1389]"
    payment_card_number_field = "[0,805][1079,805]"
    payment_save_card_button = "[300,935][310,935]"
    payment_pay_button = "[0,1205][1079,1205]"
    payment_complete_amount_fully = "[95,1431][513,1513]"

    #delivery
    delivery_pickuppoints_button = "[53,627][530,853]"
    delivery_pickuppoints_choose_button = "[53,1134][1028,1268]"
    delivery_pickuppoints_search_field = "[53,1984][1028,2089]"
    delivery_pickuppoints_search_result_first_item = "[84,620][996,806]"
    delivery_pickuppoints_found_point = "[539,1102][539,1102]"
    delivery_pickuppoints_found_point_confirm = "[289,2117][791,2277]"
    delivery_recipient_choose = "[53,937][1028,1071]"
    delivery_recipient_testuser_button = "[53,917][322,993]"
    delivery_recipient_familia_tf = "[53,962][1028,1121]"

    #custom wish
    custom_wish_name_field = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')
    custom_wish_price_field = (By.XPATH, '//android.view.View[@content-desc="Стоимость"]')
    custom_wish_description_field = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_desc_field"]')
    custom_wish_add_photo_button = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')
    custom_wish_where_to_find = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')
    custom_wish_added_first_wish = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')
    custom_wish_privacy_only_me = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')
    custom_wish_privacy_some = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')
    custom_wish_privacy_some_choose_first_friend = (By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_name_field"]')

    friend_wish_first_wish = (By.XPATH, '//android.view.View[@resource-id="friend_wish_0"]')
    friend_wish_2_wish = (By.XPATH, '//android.view.View[@resource-id="friend_wish_1"]')
    friend_wish_3_wish = (By.XPATH, '//android.view.View[@resource-id="friend_wish_2"]')

    #screenshots path
    original_avatar_ss_path = "reporting/ss/avatar.png"
    updated_avatar_ss_path = "reporting/ss/updated_avatar.png"
    main_screen_ss = "[0,210][1080,2204]"


    confirm_code = "555555555"


    cardNumber = "4545454545454545"
    cardExpDate = "2222"
    cardCVC = "777"

    #CARD_NUMBER

    #ulr
    traektoria_url = "https://www.traektoria.com/product/1243370_gornolyzhnye-palki-salomon-angel-s3-xl/"
    parseCitilink = "https://www.citilink.com/product/smartfon-huawei-pura70-ady-lx9-256gb-12gb-belyi-3g-4g-6-67-1080x2400-a-2021538/"
    parseDetmir = "https://www.detmir.com/product/index/id/4679809/?variant_id=4679809"
    parseGoldapple = "https://goldapple.com/19000266054-gentleman-society-extreme"
    parseLamoda = "https://www.lamoda.com/p/rtladr699001/shoes-adidasoriginals-krossovki/"
    parseGloria = "https://www.gloria-jeans.com/product/BOW002075-1/Cernoe-palto-oversize-s-kapusonom"
    parseLetual = "https://www.letu.com/product/dolce-gabbana-l-imperatrice-eau-de-toilette/11805"
    parseMvideo = "https://www.mvideo.com/products/stiralnaya-mashina-schulthess-spirit-540-titan-rock-4218641"
    parseMegamarket = "https://megamarket.com/catalog/details/akkumulyatornaya-bezudarnaya-drel-shurupovert-makita-df333dwye-100025805816_197022/"
    parseOzon = "https://ozon.com/product/samsung-televizor-ue55du7100ux-55-4k-uhd-chernyy-1606565854/"
    parseWildberries = "https://www.wildberries.com/catalog/176035400/detail.aspx"
    parseVseIns = "https://www.vseinstrumenti.com/product/elektricheskaya-tsepnaya-pila-gigant-sf-7j-153-3921348/"
    parseTraektoria = "https://www.traektoria.com/product/1668266_snoubord-capita-the-black-snowboard-of-death-wide/"
    parseRivgosh = "https://rivegauche.com/product/jusbox-cheeky-smile-eau-de-parfum"




    long_description = "START Ultimate Comfort Memory Foam Pillow - Your Key to a Restful Night's Sleep. Say goodbye to restless nights and wake up feeling refreshed with the Ultimate Comfort Memory Foam Pillow. This revolutionary pillow is designed to provide the perfect balance of support and softness, ensuring you get the quality sleep you deserve. Key Features: Ergonomic Design - Crafted to cradle your head and neck in any sleeping position. Whether you sleep on your back, side, or stomach, the pillow adapts seamlessly to your posture. Premium Memory Foam - Made from high-density memory foam that molds to your unique shape, providing personalized support and alleviating pressure points. Cooling Gel Technology - Integrated with cooling gel layers to regulate temperature and keep you cool throughout the night. Hypoallergenic Cover - The removable and washable cover is made of breathable, hypoallergenic fabric, perfect for those with allergies or sensitive skin. Durable and Long-Lasting - Engineered to maintain its shape and firmness, even after years of use. Benefits: Improved Sleep Quality - Reduces tossing and turning by promoting spinal alignment. Pain Relief - Relieves neck and shoulder pain, ensuring you wake up without stiffness. Better Airflow - The ventilated design prevents heat buildup, allowing for a fresher sleeping experience. Product Specifications: Dimensions - 24\" x 16\" x 5\"; Weight - 3.5 lbs; Material - High-density memory foam with gel-infused layers; Cover - Zippered polyester blend. Why Choose the Ultimate Comfort Memory Foam Pillow? Backed by thousands of 5-star reviews, this pillow is trusted by sleep experts and customers alike. It's the perfect blend of luxury and functionality, designed to enhance your overall well-being by promoting deeper, uninterrupted sleep. Don't settle for less when it comes to your rest. Upgrade to the Ultimate Comfort Memory Foam Pillow today and experience the difference! END"




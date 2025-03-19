class ErrorCode:
    EMAIL_TAKEN = "Аккаунт с такой почтой уже существует"
    EMAIL_NOT_VALID = "К сожалению, на этот электронный адрес невозможно зарегистрировать аккаунт. Используйте другую почту"
    USER_NOT_FOUND = "Пользователь не найден"
    INVALID_CONFIRMATION_CODE = "Неверный код подтверждения"
    CONFIRMATION_CODE_EXPIRED = "Срок действия кода истек"
    EMAIL_ALREADY_CONFIRMED = "Вы уже подтвердили адрес электронной почты"
    EMAIL_NOT_CONFIRMED = "Подтвердите адрес электронной почты"
    INCORRECT_OLD_PASSWORD = "Неверный пароль"
    TELEGRAM_USERNAME_OR_ID_ALREADY_EXISTS = (
        "Телеграмм аккаунт уже привязан к другому аккаунту 21YARD"
    )
    USER_PHONE_ALREADY_VERIFIED = "Номер телефона пользователя уже подтвержден"
    ADMIN_ROLE_NOT_FOUND = "Отсутствует роль админа в БД"

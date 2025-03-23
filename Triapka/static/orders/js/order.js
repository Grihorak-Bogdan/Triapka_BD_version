document.addEventListener('DOMContentLoaded', function () {
  var toggleBasketHeader = document.querySelector('.div_hide_basket');
  var basketSide = document.querySelector('.basket_side');

  function updateVisibility() {
      // Установка видимости в зависимости от ширины окна
      if (window.innerWidth <= 750) {
          toggleBasketHeader.style.display = 'block';
          basketSide.style.display = 'none';
      } else {
          toggleBasketHeader.style.display = 'none';
          basketSide.style.display = 'block';
      }
  }

  // Проверяем и обновляем видимость при загрузке страницы
  updateVisibility();

  // Обновляем видимость при изменении размера окна
  window.addEventListener('resize', updateVisibility);

  // Добавляем обработчик клика для переключения видимости корзины
  toggleBasketHeader.addEventListener('click', function () {
      if (basketSide.style.display === 'none' || basketSide.style.display === '') {
          basketSide.style.display = 'block'; // Показываем корзину, если она была скрыта
      } else {
          basketSide.style.display = 'none'; // Скрываем корзину, если она была видна
      }
  });
});
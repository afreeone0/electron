const catalogButton = document.querySelector('.catalog-button');
const dropdownMenu = document.querySelector('.dropdown-menu');
const TEMPORARY_DOMEN = 'https://127.0.0.1/'

catalogButton.addEventListener('click', () => {
    dropdownMenu.classList.toggle('show');
    const windowHeight = window.innerHeight;
    const buttonRect = catalogButton.getBoundingClientRect();
    const menuHeight = dropdownMenu.offsetHeight;
    const totalHeight = buttonRect.top + menuHeight;

  if (totalHeight > windowHeight) {
    dropdownMenu.classList.add('bottom');
  } else {
    dropdownMenu.classList.remove('bottom');
  }

});

document.addEventListener('click', (event) => {
    if(!catalogButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.remove('show');
        dropdownMenu.classList.remove('bottom');
    }
});

//document.addEventListener('DOMContentLoaded', function() {
//    const addToCartButtons = document.querySelectorAll('.add-to-cart-button');
//
//    addToCartButtons.forEach(button => {
//      button.addEventListener('click', function(event) {
//        event.preventDefault();
//        const productId = this.dataset.productId;
//        fetch(`${TEMPORARY_DOMEN}/cart/add/${productId}/`, {
//          method: 'GET',
//          headers: {
////            'X-Requested-With': 'XMLHttpRequest',
//            'Content-Type': 'application/json',
////            'X-CSRFToken': getCookie('csrftoken')
//          }
//        })
//        .then(response => {
//          if (response.ok) {
//            return response.json();
//          } else {
//            throw new Error('Ошибка сети');
//          }
//        })
//        .then(data => {
//          if (data.status === 'success') {
//            updateCartCount();
//          }
//        })
//        .catch(error => {
//          alert('Произошла ошибка при добавлении в корзину.')
//        });
//      });
//    });
//
//    function getCookie(name) {
//      let cookieValue = null;
//      if (document.cookie && document.cookie !== '') {
//        const cookies = document.cookie.split(';');
//        for (let i = 0; i < cookies.length; i++) {
//          let cookie = cookies[i].trim();
//          if (cookie.substring(0, name.length + 1) === (name + '=')) {
//            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//            break;
//          }
//        }
//      }
//      return cookieValue;
//    }
//
//    function updateCartCount() {
//      alert('SALKSKNASKJDKASDKLIO#U()*$)#(@)$#')
//    }
//
//});

var paymentForm = document.getElementById('paymentForm');

paymentForm.addEventListener('submit', payWithPaystack, false);

function payWithPaystack() {

  var handler = PaystackPop.setup({
    key: 'pk_test_7ca2670623a4247a764e0c5413be0749edf05fd1',
    email: document.getElementById('email-address').value,
    amount: document.getElementById('amount').value * 100,
    currency: 'NGN',

    callback: function(response) {
      $.ajax({
        url: '/fund-account?reference='+ response.reference,
        method: 'get',
        success: function () {
          window.location.pathname = '/index';
        }
      });
    },

    onClose: function() {

      alert('Transaction was not completed, window closed.');

    },

  });

  handler.openIframe();

}
var paymentForm = document.getElementById('paymentForm');

if (paymentForm) {

  paymentForm.addEventListener('submit', payWithPaystack, false);

  function payWithPaystack() {
  
    var handler = PaystackPop.setup({
      key: 'PAYSTACK TEST/LIVE PUBLIC KEY',
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


}

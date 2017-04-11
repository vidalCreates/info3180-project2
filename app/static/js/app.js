/* Add your Application JavaScript */
const app = angular.module('jwtproject2', []);

app.controller('jwtController', function ($scope, $http) {
  $scope.result = 'The result will appear here.';
  $scope.token = '';

  // Usually the generation of a JWT will be done when a user either registers
  // with your web application or when they login.
  $scope.getToken = function() {
    $http.get('/api/users/login')
      .then(function(response) {
        let jwt_token = response.data.data.token;

        // We store this token in localStorage so that subsequent API requests
        // can use the token until it expires or is deleted.
        localStorage.setItem('token', jwt_token);
        console.info('Token generated and added to localStorage.');\
        console.log('Token generated and added to localStorage.');
        $scope.token = jwt_token;
      });
  };

  // Remove token stored in localStorage.
  // Usually you will remove it when a user logs out of your web application
  // or if the token has expired.
  $scope.removeToken = function() {
    localStorage.removeItem('token');
    console.info('Token removed from localStorage.');
    alert('Token removed!');
  };

  // The /api/secure route requires a JWT token be sent via an Authorization
  // header. JWT also needs to use the 'Bearer' schema.
  $scope.getSecure = function() {
    $http.get('/api/secure', {
      'headers': {
        // Try it with the `Basic` schema and you will see it gives an error message.
        'Authorization': 'Basic ' + localStorage.getItem('token')

        // JWT requires the Authorization schema to be `Bearer` instead of `Basic`
        // 'Authorization': 'Bearer ' + localStorage.getItem('token')
      }
    }).then(function(response) {
      let alert = document.querySelector('.alert');
      alert.classList.remove('alert-info', 'alert-danger');
      alert.classList.add('alert-success');

      let result = response.data;
      // successful response
      $scope.result = `Congrats! You have now made a successful request with a JSON Web Token. Name is: ${result.data.user.name}.`;
    }, function(response) {
      let alert = document.querySelector('.alert');
      alert.classList.remove('alert-info');
      alert.classList.add('alert-danger');

      // unsuccessful response (ie. there was an error)
      $scope.result = `There was an error. ${response.data.description}`;
    });
  };

  // Visit the unsecure route which doesn't need a JWT token or
  // Authorization header
  $scope.getUnsecure = function() {
    $http.get('/api/unsecure').then(function(response) {
      let result = response.data;
      $scope.result = `You visited the unsecure route that didn't require a JSON Web Token. Name is: ${result.data.user.name}.`;
    });
  };
});/* Add your Application JavaScript */
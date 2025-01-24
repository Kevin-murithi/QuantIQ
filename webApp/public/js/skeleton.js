const toggler = document.querySelector('.toggler');

toggler.addEventListener('click', () => {
  document.querySelector('.skeleton').classList.toggle('active');
  //document.querySelector('.parent_container').classList.toggle('respond');
})
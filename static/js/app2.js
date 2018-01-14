function alertone()
{
document.addEventListener('DOMContentLoaded', function () {
  if (Notification.permission !== "granted")
    Notification.requestPermission();
});

if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification('Authentication', {
      icon: 'http://cdn.sstatic.net/stackexchange/img/logos/so/so-icon.png',
      body: "Invalid Username",
    });
}
}
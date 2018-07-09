export default {
  items: [
    {
      title: true,
      name: 'メニュー',
      wrapper: {            // optional wrapper object
        element: '',        // required valid HTML5 element tag
        attributes: {}        // optional valid JS object with JS API naming ex: { className: "my-class", style: { fontFamily: "Verdana" }, id: "my-id"}
      },
      class: ''             // optional class names space delimited list for title item ex: "text-center"
    },
    {
      name: 'マイページ',
      url: '/mypage',
      icon: 'icon-star',
    },
    {
      name: 'プロフィール',
      url: '/mypage',
      icon: 'icon-user',
    },
    {
      name: 'ログアウト',
      url: '/mypage',
      icon: 'icon-logout',
    },
  ],
};

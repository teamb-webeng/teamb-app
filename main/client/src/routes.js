import React from 'react';
import Loadable from 'react-loadable'

function Loading() {
  return <div>Loading...</div>;
}

const Mypage = Loadable({
  loader: () => import('./views/Mypage/Mypage'),
  loading: Loading,
});

// https://github.com/ReactTraining/react-router/tree/master/packages/react-router-config
const routes = [
  { path: '/mypage', name: 'Mypage', component: Mypage },
];

export default routes;

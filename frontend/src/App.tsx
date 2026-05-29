import MainPage from "./pages/MainPage";

/**
 * 단일 메인 화면.
 *
 * 필요 시 향후 별도 라우트(/documents/:documentNo 등)를 추가할 수 있도록
 * pages/ 폴더에 페이지 컴포넌트를 두고, 여기서는 진입점만 담당한다.
 */
function App() {
  return <MainPage />;
}

export default App;

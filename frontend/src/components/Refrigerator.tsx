import NavBar from './NavBar'
import ProductList from './ProductList'
import VideoInput from './VideoInput'

const Refrigerator = () => {
    return(
      <div className="container">
        <NavBar />
        <ProductList />
        <VideoInput />
      </div>
    )
}

export default Refrigerator;
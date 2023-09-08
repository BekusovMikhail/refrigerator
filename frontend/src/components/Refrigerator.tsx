import { useState, useEffect } from 'react';
import NavBar from './NavBar'
import ProductList from './ProductList'
import VideoInput from './VideoInput'

const Refrigerator = () => {
    const [cameraId, setCameraId] = useState<number>(0)

    return(
      <div className="container">
        <NavBar />
        <ProductList cameraId={cameraId} setCameraId={setCameraId}/>
        <VideoInput cameraId={cameraId}/>
      </div>
    )
}

export default Refrigerator;
import lanzaroteImg from '../assets/lanzarote-hi-res.jpg'
import { Rating } from '../rating'

export function MapView() {
    return <>
        <img src={lanzaroteImg} className="base-image" alt="Lanzarote" />
        <Rating/>
    </>
}
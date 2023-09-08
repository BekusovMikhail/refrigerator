import { Text } from "@chakra-ui/react";
import {
    useQuery
  } from '@tanstack/react-query'

const getProducts = async (product_id: number) => {
    const response = await fetch(`http://localhost:8000/api/product_name_by_id/${product_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
    })
    return response.json()
}

function useProducts(product_id: number) {
    return useQuery({
        queryKey: ['products'],
        queryFn: () => getProducts(product_id),
    })
}

const Product = ({id}: {id: number}) => {
    const { status, data, isFetching } = useProducts(id)

    return(
        <div>
            {status === 'loading' ? (
                'Loading...'
                ) : status === 'error' ? (
                <span>Error</span>
                ) : (
                    <Text>
                        {data["product"]}
                    </Text>
                )}
        </div>
    )
}

export default Product;
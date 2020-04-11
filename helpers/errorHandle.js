
export const errorHandle = (err, req, res, next) => {
    return typeof (err) === 'string' ? res.status(400).json({message: err}) : res.status(500).json({message: err})
}
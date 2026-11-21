const { getRate } = require('./_rate');
module.exports = async (req, res) => {
  const r = await getRate();
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=600');
  res.end(JSON.stringify(r ? { rate: r.rate, updatedAt: r.updatedAt } : { rate: null }));
};

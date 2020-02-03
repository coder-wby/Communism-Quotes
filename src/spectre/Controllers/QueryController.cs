using System.Collections.Generic;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;

namespace spectre.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class QueryController : ControllerBase
    {
        [HttpGet("{qry?}")]
        public IEnumerable<string> Get(string qry)
        {
            if (qry == null)
                return new[] {"no query"};

            var ret = new List<string> {$"result for {qry}:"};
            for (int i = 0; i < 10; i++)
                ret.Add($"result {i + 1}");
            ret.Add($" 以上是关键字[{qry}]搜索的结果");

            return ret;
        }
    }
}
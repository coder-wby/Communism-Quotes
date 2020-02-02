using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;

namespace spectre.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class QueryController : ControllerBase
    {
        [HttpGet("/[controller]/{qry?}")]
        public IEnumerable<string> Get(string qry)
        {
            if (qry == null)
                return new[] {"no query"};

            var ret = new List<string> {$"result for {qry}:"};
            for (int i = 0; i < 10; i++)
            {
                ret.Add($"result {i + 1}");
            }

            return ret;
        }
    }
}